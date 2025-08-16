"""
OpenAI Cost Tracker

A Python package for tracking and estimating costs when using OpenAI API.
Provides cost estimation, usage tracking, and detailed reporting for OpenAI API calls.
"""

from .cost_estimator import CostEstimator, AsyncCostEstimator
from .schemas import ModelTotals, Totals
from .constants import PRICES_USD_PER_MLN_TOKEN
from .utils import _extract_usage_and_model, _calc_cost

__version__ = "0.0.1"
__author__ = "Timur Zhilyaev"

__all__ = [
    "CostEstimator",
    "AsyncCostEstimator", 
    "ModelTotals",
    "Totals",
    "PRICES_USD_PER_MLN_TOKEN",
    "_extract_usage_and_model",
    "_calc_cost"
]


