from typing import Any, Optional, Tuple
from decimal import Decimal
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.responses import Response
from .constants import PRICES_USD_PER_MLN_TOKEN

def _extract_usage_and_model(resp: ChatCompletion | Response) -> Tuple[Optional[str], int, int, int, int]:
    """
    Пытается вытащить (model, in, out, total) из ответа SDK.
    Поддерживает Responses API (input/output_tokens) и Chat Completions (prompt/completion/total_tokens).
    Возвращает (model|None, in_tokens, out_tokens, cached_tokens, total_tokens).
    """
    # pydantic-подобные объекты:
    model = getattr(resp, "model", None)
    usage = getattr(resp, "usage", None)

    # dict-ответ?
    if usage is None and isinstance(resp, dict):
        model = resp.get("model", model)
        usage = resp.get("usage")

    in_tok = out_tok = total_tok = 0
    if usage:
        # Responses API
        if hasattr(usage, "input_tokens") or (isinstance(usage, dict) and "input_tokens" in usage):
            val = usage if isinstance(usage, dict) else usage.__dict__
            in_tok = int(val.get("input_tokens", 0) or 0)
            out_tok = int(val.get("output_tokens", 0) or 0)
            cached_tok = int(val.get("cached_tokens", 0) or 0)
            total_tok = int(val.get("total_tokens", in_tok + out_tok) or (in_tok + out_tok))
            
        # Chat Completions / Embeddings
        elif hasattr(usage, "prompt_tokens") or (isinstance(usage, dict) and "prompt_tokens" in usage):
            val = usage if isinstance(usage, dict) else usage.__dict__
            prompt_tokens_details = val.get("prompt_tokens_details", {})
            in_tok = int(val.get("prompt_tokens", 0) or 0)
            out_tok = int(val.get("completion_tokens", 0) or 0)
            cached_tok = int(getattr(prompt_tokens_details, "cached_tokens", 0) or 0)
            total_tok = int(val.get("total_tokens", in_tok + out_tok) or (in_tok + out_tok))
            
    return model, in_tok, out_tok, cached_tok, total_tok


def _calc_cost(model: Optional[str], in_tok: int, out_tok: int, cached_tok: int) -> Decimal:
    if not model:
        return Decimal("0.0")
    price = PRICES_USD_PER_MLN_TOKEN.get(model)
    if not price:
        # Неизвестная модель — считаем как 0, но можно логировать/кидать warning.
        return Decimal("0.0")
    
    # Convert to USD per token
    price = {k: (v / 1_000_000) for k, v in price.items()}
    
    return Decimal(in_tok) * Decimal(price.get("input", 0.0)) + Decimal(out_tok) * Decimal(price.get("output", 0.0)) + Decimal(cached_tok) * Decimal(price.get("cached", 0.0))


