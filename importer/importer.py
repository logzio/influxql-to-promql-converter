from abc import abstractmethod
from base_module.module import Module


class Importer(Module):

    def __init__(self, module_name, log_level):
        super().__init__(module_name, log_level)

    @abstractmethod
    def fetch_dashboards(self) -> list[dict]:
        pass
