#!/usr/bin/env python3
"""
Simple test script to verify the package can be imported correctly.
"""

def test_imports():
    """Test that all main components can be imported."""
    try:
        from openai_cost_tracker import CostEstimator, AsyncCostEstimator
        from openai_cost_tracker import ModelTotals, Totals
        from openai_cost_tracker import PRICES_USD_PER_MLN_TOKEN
        print("✓ All imports successful!")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_schemas():
    """Test that the data models work correctly."""
    try:
        from openai_cost_tracker import ModelTotals, Totals
        
        # Test ModelTotals
        model_totals = ModelTotals(
            input_tokens=1000,
            output_tokens=500,
            cost_usd=0.01
        )
        print(f"✓ ModelTotals created: {model_totals}")
        
        # Test Totals
        totals = Totals()
        totals.per_model["gpt-4o-mini"] = model_totals
        print(f"✓ Totals created: {totals}")
        print(f"✓ Total cost: ${totals.cost_usd}")
        
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI Cost Tracker package...")
    print("-" * 40)
    
    success = True
    success &= test_imports()
    success &= test_schemas()
    
    print("-" * 40)
    if success:
        print("🎉 All tests passed! Package is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
