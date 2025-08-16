from ..schemas import Totals

class BaseOutput:
    def output(self, totals: Totals) -> None:
        raise NotImplementedError()


