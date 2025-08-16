from typing import Dict

PRICES_USD_PER_MLN_TOKEN: Dict[str, Dict[str, float]] = {
    # GPT 5
    "gpt-5":       {"input": 1.00, "cached": 0.13, "output": 10.00},
    "gpt-5-nano":  {"input": 0.05, "cached": 0.01, "output": 0.40},
    "gpt-5-mini":  {"input": 0.25, "cached": 0.03, "output": 2.00},
    
    # GPT 4.1
    "gpt-4.1": {"input": 2.00, "cached": 0.50, "output": 8.00},
    
    # GPT 4
    "gpt-4o":      {"input": 2.50, "cached": 1.25, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "cached": 0.08, "output": 0.60},
}


