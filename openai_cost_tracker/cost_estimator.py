# cost_estimator.py
from __future__ import annotations
import asyncio
from typing import Any, Dict, Optional
from openai import OpenAI, AsyncOpenAI, Client, AsyncClient
from decimal import getcontext
import logging

from ._proxy import _ClientProxy, _AsyncClientProxy
from .constants import PRICES_USD_PER_MLN_TOKEN
from .schemas import ModelTotals, Totals
from .utils import _extract_usage_and_model, _calc_cost
from .output.base import BaseOutput
from .output.simple import SimplePrintOutput

getcontext().prec = 6

logger = logging.getLogger(__name__)
    
class CostEstimator:
    """
    Usage example:
    ```python
    client = OpenAI(api_key=...)
    async with CostEstimator(client, prices=...) as estimator:
        r = estimator.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Answer to the Ultimate Question of Life, the Universe, and Everything?"}],
        )
        
    # at exit: print report including cost of all requests
    === OpenAI Cost Summary ===
    Total cost: $10.00
    Tokens: in=1000000  out=1000000  cached=0  total=2000000
    By model:
      - gpt-4o: $10.00  (in=1000000, out=1000000, cached=0, total=2000000)
    ```
    """

    def __init__(
        self,
        client: OpenAI | Client,
        custom_prices: Optional[Dict[str, Dict[str, float]]] = None,
        custom_output: Optional[BaseOutput] = None,
    ):
        self._orig = client
        self._prices = custom_prices or PRICES_USD_PER_MLN_TOKEN
        self.totals = Totals()
        self._output = custom_output or SimplePrintOutput()
        
    async def __aenter__(self):
        # Create client proxy
        def on_response(resp: Any, call_kwargs: dict):
            logger.debug(f'on_response {resp} {call_kwargs}')
            model, in_tok, out_tok, cached_tok, total_tok = _extract_usage_and_model(resp)
            logger.debug(f'model {model} in_tok {in_tok} out_tok {out_tok} cached_tok {cached_tok} total_tok {total_tok}')
            
            # If model is not returned in the response — try to get it from kwargs
            model = call_kwargs.get("model")
            if (in_tok + out_tok + total_tok) == 0:
                return
            cost = _calc_cost(model, in_tok, out_tok, cached_tok)
            logger.debug(f'cost {cost}')
            
            m = self.totals.per_model.setdefault(model or "<unknown>", ModelTotals())
            m.input_tokens += in_tok
            m.output_tokens += out_tok
            m.cached_tokens += cached_tok
            m.total_tokens += total_tok or (in_tok + out_tok)
            m.cost_usd += cost
            
            logger.debug(f'self.totals {self.totals}')
            logger.debug(f'm {m}')
            
        self._proxy = _ClientProxy(self._orig, on_response)
        
        return self._proxy

    async def __aexit__(self, exc_type, exc, tb):
        self._output.output(self.totals)
        # Do nothing
        return False

class AsyncCostEstimator:
    """
    Usage example:
    ```python
    client = AsyncOpenAI(api_key=...)
    async with AsyncCostEstimator(client, prices=...) as estimator:
        r = await estimator.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Answer to the Ultimate Question of Life, the Universe, and Everything?"}],
        )
        
    # at exit: print report including cost of all requests
    === OpenAI Cost Summary ===
    Total cost: $10.00
    Tokens: in=1000000  out=1000000  cached=0  total=2000000
    By model:
      - gpt-4o: $10.00  (in=1000000, out=1000000, cached=0, total=2000000)
    ```
    """

    def __init__(
        self,
        client: AsyncOpenAI | AsyncClient,
        custom_prices: Optional[Dict[str, Dict[str, float]]] = None,
        custom_output: Optional[BaseOutput] = None,
    ):
        self._orig = client
        self._lock = asyncio.Lock()
        self.totals = Totals()
        self._tasks = []
        
        self._prices = custom_prices or PRICES_USD_PER_MLN_TOKEN
        self._output = custom_output or SimplePrintOutput()

    async def __aenter__(self):
        # Create client proxy
        def on_response(resp: Any, call_kwargs: dict):
            logger.debug(f'on_response {resp} {call_kwargs}')
            model, in_tok, out_tok, cached_tok, total_tok = _extract_usage_and_model(resp)
            logger.debug(f'model {model} in_tok {in_tok} out_tok {out_tok} cached_tok {cached_tok} total_tok {total_tok}')
            
            # If model is not returned in the response — try to get it from kwargs
            model = call_kwargs.get("model")
            if (in_tok + out_tok + total_tok) == 0:
                return
            cost = _calc_cost(model, in_tok, out_tok, cached_tok)
            logger.debug(f'cost {cost}')
            
            # Atomically accumulate
            async def upd():
                m = self.totals.per_model.setdefault(model or "<unknown>", ModelTotals())
                m.input_tokens += in_tok
                m.output_tokens += out_tok
                m.cached_tokens += cached_tok
                m.total_tokens += total_tok or (in_tok + out_tok)
                m.cost_usd += cost
                
                logger.debug(f'self.totals {self.totals}')
                logger.debug(f'm {m}')
                
            # Update under lock, to survive concurrent calls
            async def _upd_locked():
                async with self._lock:
                    await upd()
                    
            loop = asyncio.get_running_loop()
            self._tasks.append(loop.create_task(_upd_locked()))

        # Create client proxy
        self._proxy = _AsyncClientProxy(self._orig, on_response)
        
        return self._proxy

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.gather(*self._tasks)
        self._output.output(self.totals)
        
        # Do nothing
        return False


