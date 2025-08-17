from typing import Any, Callable
import inspect
import logging

logger = logging.getLogger(__name__)

class _ClientProxy:
    """
    Transparent proxy over OpenAI client.
    Any function call is intercepted and, if the response has usage, it is counted.
    Also wraps stream objects to catch the final usage.
    """

    def __init__(self, obj: Any, on_response: Callable[[Any, dict], None]):
        self.__dict__["_obj"] = obj
        self.__dict__["_on_resp"] = on_response

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._obj, name)

        if callable(attr):
            def wrapper(*args, **kwargs):
                res = attr(*args, **kwargs)

                # IMPORTANT: the method could return a coroutine — check the result
                if inspect.isawaitable(res):
                    async def _await_and_handle():
                        real = await res
                        self._handle_result(real, kwargs)
                        return self.__dict__.get("_last_result", real)
                    return _await_and_handle()

                # sync result
                self._handle_result(res, kwargs)
                return self.__dict__.get("_last_result", res)

            return wrapper

        # Resource (chat, responses, etc.)
        return _ClientProxy(attr, self._on_resp)

    def __setattr__(self, name, value):
        return setattr(self._obj, name, value)

    def _handle_result(self, res: Any, call_kwargs: dict):
        """
        1) If res is a stream object, wrap it in _StreamProxy and return it outside.
        2) If a regular response, count usage immediately.
        """
        # stream object is identified by the presence of get_final_response or "stream"
        if hasattr(res, "get_final_response") or hasattr(res, "__aiter__") or hasattr(res, "__iter__"):
            logger.debug('processing stream')
            # Replace res with the caller (return) — for this we do a trick:
            def on_final(final_resp: Any):
                self._on_resp(final_resp, call_kwargs)
            proxy = _StreamProxy(res, on_final)
            # Hack: return exactly proxy instead of res. To do this, we put it in _last_result
            self.__dict__["_last_result"] = proxy
            # To make the calling code see exactly proxy, we replace the returned value in the wrapper (see above).
            # Here we just save it in the field; the actual replacement is already made in wrapped/awrapped.
            # But for this to work, wrapped/awrapped must return self._last_result.
            if inspect.iscoroutinefunction(getattr(self._obj, "dummy", lambda: None)):
                pass  # no-op; just for symmetry
            # Intercept the result in the wrapper — see below.
        else:
            # Regular response — count usage immediately
            logger.debug('processing stream')
            self._on_resp(res, call_kwargs)

    # Override calls to actually return the stream proxy if it appeared in _handle_result:
    def __call__(self, *args, **kwargs):
        res = self._obj(*args, **kwargs)
        self._handle_result(res, kwargs)
        return getattr(self, "_last_result", res)

    async def __acall__(self, *args, **kwargs):
        res = await self._obj(*args, **kwargs)
        self._handle_result(res, kwargs)
        return getattr(self, "_last_result", res)

class _AsyncClientProxy:
    def __init__(self, obj: Any, on_response: Callable[[Any, dict], None]):
        self.__dict__["_obj"] = obj
        self.__dict__["_on_resp"] = on_response
        
    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._obj, name)
        logger.debug(f'attr {attr}')
        if callable(attr):
            async def wrapper(*args, **kwargs):
                res = await attr(*args, **kwargs)
                self._handle_result(res, kwargs)
                return getattr(self, "_last_result", res)
            return wrapper
        return _AsyncClientProxy(attr, self._on_resp)
        
    def __setattr__(self, name, value):
        return setattr(self._obj, name, value)
    
    def _handle_result(self, res: Any, call_kwargs: dict):
        self._on_resp(res, call_kwargs)

class _StreamProxy:
    """
    Wrapper over stream objects SDK (both sync and async),
    to catch the final response and usage.
    """

    def __init__(self, stream_obj: Any, on_final: Callable[[Any], None]) -> None:
        self._s = stream_obj
        self._on_final = on_final
        self._counted = False

    # --- Делегирование атрибутов ---
    def __getattr__(self, name: str) -> Any:
        return getattr(self._s, name)

    # --- Итерация (sync) ---
    def __iter__(self):
        return iter(self._s)

    # --- Итерация (async) ---
    def __aiter__(self):
        return self._s.__aiter__()

    # --- Контекст (sync) ---
    def __enter__(self):
        if hasattr(self._s, "__enter__"):
            return self.__class__(self._s.__enter__(), self._on_final)
        return self

    def __exit__(self, exc_type, exc, tb):
        # Попытаться считать финальный ответ
        try:
            if hasattr(self._s, "get_final_response"):
                final = self._s.get_final_response()
                self._on_final(final)
                self._counted = True
        finally:
            if hasattr(self._s, "__exit__"):
                return self._s.__exit__(exc_type, exc, tb)

    # --- Контекст (async) ---
    async def __aenter__(self):
        if hasattr(self._s, "__aenter__"):
            inner = await self._s.__aenter__()
            return self.__class__(inner, self._on_final)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if hasattr(self._s, "get_final_response"):
                final = await self._maybe_await(self._s.get_final_response())
                self._on_final(final)
                self._counted = True
        finally:
            if hasattr(self._s, "__aexit__"):
                return await self._s.__aexit__(exc_type, exc, tb)

    async def _maybe_await(self, v):
        if inspect.isawaitable(v):
            return await v
        return v


