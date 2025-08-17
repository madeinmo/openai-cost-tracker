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
    
    # o3
    "o3-pro": {"input": 20.00, "cached": 20.00, "output": 80.00},
    "o3": {"input": 2.00, "cached": 0.5, "output": 8.00},
    "o3-mini": {"input": 1.10, "cached": 0.55, "output": 4.40},
    
    # o1
    "o1-pro": {"input": 150.00, "cached": 150.0, "output": 600.00},
    "o1": {"input": 15.00, "cached": 7.50, "output": 60.00},
    "o1-mini": {"input": 1.10, "cached": 0.55, "output": 4.40},
    "o1-preview": {"input": 15.00, "cached": 7.50, "output": 60.00},
    
    # Embeddings
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    
    # Perplexity
    "sonar": {"input": 1.0, "output": 1.0},
    "sonar-pro": {"input": 3.0, "output": 15.0},
    "sonar-reasoning": {"input": 1.0, "output": 5.0},
    "sonar-reasoning-pro": {"input": 2.0, "output": 8.0},
    "sonar-deep-research": {"input": 2.0, "output": 8.0},
}