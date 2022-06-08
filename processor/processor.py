from abc import abstractmethod
from base_module.module import Module


class Processor(Module):

    def __init__(self, module_name, log_level):
        super().__init__(module_name, log_level)
        self._json_report = {}

    @abstractmethod
    def process(self, metric_and_object: list[()]) -> list[()]:
        pass

    def replace_metric(self, old_metric, new_metric, dashboard_to_panels):
        dashboards = []
        if len(dashboard_to_panels) > 0:
            for dashboard, panels in dashboard_to_panels.items():
                for panel in panels:
                    panel['expr'] = panel['expr'].replace(old_metric, new_metric)
                    self._logger.debug(f'Replaced metrics: {old_metric} ---> {new_metric} in dashboard {dashboard}')
                dashboards.append(dashboard)
            for dashboard in dashboards:
                del dashboard_to_panels[dashboard]
        if len(dashboards) == 0:
            del dashboards

    def add_to_report(self, dashboard_name, module_name, report_object):
        short_module_name = module_name.split('.')[len(module_name.split('.')) - 1]
        try:
            self._json_report[dashboard_name][short_module_name].append(report_object)
        except KeyError:
            if self._json_report.get(dashboard_name) is None:
                self._json_report[dashboard_name] = {}
            self._json_report[dashboard_name][short_module_name] = []
            self._json_report[dashboard_name][short_module_name].append(report_object)

    @abstractmethod
    def create_report_object(self, dashboard_name, old_metric, new_metric, *args) -> dict:
        pass

    def get_json_report(self) -> dict:
        return self._json_report
