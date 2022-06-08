import json
import logging
import os
from ..exporter import Exporter


class FolderExporter(Exporter):
    def __init__(self, params, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        try:
            self._path = params['path']
        except KeyError as e:
            raise ValueError(e)

    def export_dashboards(self, dashboards: list):
        if not os.path.isdir(self._path):
            try:
                os.mkdir(self._path)
            except OSError:
                self._logger.error("An error occurred while creating dashboard folder, skipping folder export")
                return
        for dashboard in dashboards:
            # Remove invalid filename character
            new_filename = dashboard['title'].replace("/", " ") + " promql.json"
            new_file = open(self._path + "/" + new_filename, "w")
            new_file.write(json.dumps(dashboard, indent=4, sort_keys=True))
            new_file.close()
            self._logger.debug(f"Successfully exported dashboard {dashboard['title']} to folder")
