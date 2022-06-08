import logging
import os
import json
from ..importer import Importer


class FolderImporter(Importer):

    def __init__(self, params: dict, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        self._path = params['path']

    def fetch_dashboards(self):
        dashboards = []
        if os.path.isdir(self._path):
            for filename in [file for file in os.listdir(self._path) if file.endswith('.json')]:
                try:
                    dashboard = json.load(open(self._path + "/" + filename))
                    dashboards.append(dashboard)
                except Exception as e:
                    super()._logger.error(f"Failed opening file: {filename}, error: {str(e)}")
                    continue
        else:
            super()._logger.error(f"Invalid folder path. Could not extract dashboards from: {self._path}")
        return dashboards
