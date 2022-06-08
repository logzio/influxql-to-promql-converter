import logging
import copy
from ..processor import Processor


class ReplaceMetricsNamesProcessor(Processor):

    def __init__(self, params, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        self._replace_map = params

    def process(self, metrics_to_objects) -> list[()]:
        filtered_metric_to_objects = copy.deepcopy(metrics_to_objects)
        for item in self._replace_map:
            if metrics_to_objects.get(item['name']):
                for dashboard in metrics_to_objects[item['name']]:
                    self.replace_metric(item['name'], item['value'], filtered_metric_to_objects[item['name']])
                    self.add_to_report(dashboard, __name__, self.create_report_object(item['name'], item['value']))
        return filtered_metric_to_objects

    def create_report_object(self, old_metric, new_metric, *args) -> dict:
        return {"converted": f"{old_metric} --> {new_metric}"}
