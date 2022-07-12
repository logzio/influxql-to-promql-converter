import json
import logging
import uuid
from datetime import datetime

import requests

from ..exporter import Exporter


class GrafanaExporter(Exporter):

    def __init__(self, params, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        try:
            self._api_endpoint = params['endpoint']
            self._auth_header_key = params['auth_header']['key']
            self._auth_header_value = params['auth_header']['value']
            self._api_headers = {
                self._auth_header_key: self._auth_header_value,
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
                'User-Agent': None
            }
        except KeyError as e:
            raise ValueError(str(e))

    def export_dashboards(self, dashboards: list):
        folder_uid = self._create_migration_folder()
        for dashboard in dashboards:
            self.export_dashboard(dashboard, folder_uid)

    # Creates dashboard in grafana
    def export_dashboard(self, dashboard, folder_uid):
        dashboard["id"] = "null"
        dashboard["uid"] = str(uuid.uuid4())
        dashboard_json = {
            "dashboard": dashboard,
            "folderUid": str(folder_uid),
            "overwrite": True
        }

        response = requests.post(self._api_endpoint + '/dashboards/db', data=json.dumps(dashboard_json),
                                 headers=self._api_headers)
        if response.status_code != 200:
            self._logger.error(f"Error creating dashboard {dashboard['title']}: {response.content}")
        else:
            self._logger.debug(f"Successfully exported dashboard: {dashboard['title']}")

    def _create_migration_folder(self):
        create_folder_url = self._api_endpoint + '/folders'
        current_datetime = datetime.now()
        dt_string = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        folder_uid = uuid.uuid4()
        folder_uid_string = str(folder_uid)
        folder_name = f"Migrated Dashboards - {dt_string}"
        request_json = {"title": folder_name, "uid": folder_uid_string}
        response = requests.post(create_folder_url, data=json.dumps(request_json), headers=self._api_headers)
        if response.status_code != 200:
            self._logger.error(f"Error creating dashboards folder: {response.content}")
        else:
            self._logger.debug(f"Successfully created migration folder in grafana, with name: {folder_name}")
        return folder_uid
