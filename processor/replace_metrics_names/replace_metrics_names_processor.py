import logging
import copy
from ..processor import Processor


class ReplaceMetricsNamesProcessor(Processor):

    def __init__(self, params, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        self._replace_map = params

    def process(self, metrics_to_objects) -> list[()]:
        dashboards_to_remove = []
        for item in self._replace_map:
            if metrics_to_objects.get(item['name']):
                for dashboard in metrics_to_objects[item['name']]:
                    dashboards_to_remove += self.replace_metric(item['name'], item['value'],
                                                                metrics_to_objects[item['name']])

                    self.add_to_report(dashboard, __name__, self.create_report_object(item['name'], item['value']))
            self.remove_updated_dashboards_from_metric_to_object(dashboards_to_remove,
                                                                 metrics_to_objects[item['name']])
        return metrics_to_objects

    def create_report_object(self, old_metric, new_metric, *args) -> dict:
        return {"converted": f"{old_metric} --> {new_metric}"}
