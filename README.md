# OpenAI Cost Tracker

A Python package for tracking and estimating costs when using OpenAI API. Provides cost estimation, usage tracking, and detailed reporting for OpenAI API calls.

## Features

- **Cost Tracking**: Automatically track token usage and costs for OpenAI API calls
- **Real-time Estimation**: Calculate costs based on current OpenAI pricing
- **Multiple Models**: Support for GPT-4, GPT-5, and other OpenAI models
- **Async Support**: Full async/await support for modern Python applications
- **Detailed Reporting**: Comprehensive cost summaries and usage statistics
- **Easy Integration**: Drop-in replacement for OpenAI client with automatic cost tracking

## Installation

### From Source

```bash
git clone <repository-url>
cd openai-cost-tracker
pip install -e .
```

### Using pip

```bash
pip install git+https://github.com/madeinmo/openai-cost-tracker.git
```

## Quick Start

### Basic Usage

```python
from openai import OpenAI
from openai_cost_tracker import CostEstimator

# Create your OpenAI client
client = OpenAI(api_key="your-api-key")

# Wrap with cost estimator
async with CostEstimator(client) as estimator:
    response = estimator.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, how are you?"}]
    )

# Cost summary is automatically printed when exiting the context
```

### Async Usage

```python
from openai import AsyncOpenAI
from openai_cost_tracker import AsyncCostEstimator

async def main():
    client = AsyncOpenAI(api_key="your-api-key")
    
    async with AsyncCostEstimator(client) as estimator:
        response = await estimator.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, how are you?"}]
        )
    
    # Cost summary is automatically printed

asyncio.run(main())
```

## API Reference

### CostEstimator

Main class for synchronous OpenAI client cost tracking.

```python
class CostEstimator:
    def __init__(
        self,
        client: OpenAI,
        custom_prices: Optional[Dict[str, Dict[str, float]]] = None,
        custom_output: Optional[BaseOutput] = None,
    )
```

**Parameters:**
- `client`: OpenAI client instance
- `custom_prices`: Optional custom pricing dictionary
- `custom_output`: Optional custom output handler

### AsyncCostEstimator

Async version for AsyncOpenAI client cost tracking.

```python
class AsyncCostEstimator:
    def __init__(
        self,
        client: AsyncOpenAI,
        custom_prices: Optional[Dict[str, Dict[str, float]]] = None,
        custom_output: Optional[BaseOutput] = None,
    )
```

### Data Models

#### ModelTotals

```python
@dataclass
class ModelTotals:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Decimal = Decimal("0.0")
```

#### Totals

```python
@dataclass
class Totals:
    per_model: Dict[str, ModelTotals] = field(default_factory=dict)
    
    @property
    def cost_usd(self) -> Decimal
    @property
    def input_tokens(self) -> int
    @property
    def output_tokens(self) -> int
    @property
    def total_tokens(self) -> int
```

## Pricing

The package includes up-to-date pricing for OpenAI models:

- **GPT-5**: $1.00/1M input, $10.00/1M output, $0.13/1M cached
- **GPT-5-nano**: $0.05/1M input, $0.40/1M output, $0.01/1M cached
- **GPT-5-mini**: $0.25/1M input, $2.00/1M output, $0.03/1M cached
- **GPT-4.1**: $2.00/1M input, $8.00/1M output, $0.50/1M cached
- **GPT-4o**: $2.50/1M input, $10.00/1M output, $1.25/1M cached
- **GPT-4o-mini**: $0.15/1M input, $0.60/1M output, $0.08/1M cached

## Customization

### Custom Pricing

```python
custom_prices = {
    "gpt-4o": {"input": 2.00, "cached": 1.00, "output": 8.00}
}

async with CostEstimator(client, custom_prices=custom_prices) as estimator:
    # Use custom pricing
```

### Custom Output

```python
from openai_cost_tracker.output.base import BaseOutput

class CustomOutput(BaseOutput):
    def output(self, totals: Totals):
        # Custom output logic
        pass

async with CostEstimator(client, custom_output=CustomOutput()) as estimator:
    # Use custom output handler
```

## Development

### Setup Development Environment

```bash
git clone <repository-url>
cd openai-cost-tracker
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.

## Support the Project

If you enjoy using this project and would like to help it grow, consider showing your support!  
A star on GitHub, sharing with others, or any kind words are always appreciated.

USDT TRC20 - TJ5GUbqJ51UDSKb2ZNQM3jHLL7DcjENWRs