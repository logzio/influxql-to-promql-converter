from abc import abstractmethod
from base_module.module import Module


class Exporter(Module):

    def __init__(self, module_name, log_level):
        super().__init__(module_name, log_level)

    @abstractmethod
    def export_dashboards(self, dashboards: list):
        pass
