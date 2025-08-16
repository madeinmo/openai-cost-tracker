from .base import BaseOutput
from ..schemas import Totals

class SimplePrintOutput(BaseOutput):
    def __init__(self, title: str = "OpenAI Cost Summary"):
        self._title = title
        
    def output(self, totals: Totals) -> None:
        # Print short report
        lines = []
        lines.append(f"=== {self._title} ===")
        lines.append(f"Total cost: ${totals.cost_usd}")
        lines.append(f"Tokens: in={totals.input_tokens:,}  out={totals.output_tokens:,}  cached={totals.cached_tokens:,}  total={totals.total_tokens:,}")
        
        if totals.per_model:
            lines.append("By model:")
            for model, m in totals.per_model.items():
                lines.append(
                    f"  - {model}: ${m.cost_usd}  "
                    f"(in={m.input_tokens:,}, out={m.output_tokens:,}, cached={m.cached_tokens:,}, total={m.total_tokens:,})"
                )
        print("\n".join(lines))


