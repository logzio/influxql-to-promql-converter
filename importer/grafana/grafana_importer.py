import logging

from ..importer import Importer
import json
import requests


class GrafanaImporter(Importer):
    API_HEADERS = {'Authorization': "",
                   'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, params: dict, log_level=logging.INFO):
        super().__init__(__name__, log_level)
        try:
            self._grafana_endpoint = params['endpoint']
            self._grafana_api_token = params['api_token']
            self.API_HEADERS['Authorization'] = 'Bearer ' + self._grafana_api_token
        except KeyError as e:
            raise ValueError(str(e))

    def fetch_dashboards(self):
        dashboards = self._build_dashboards_list()
        return dashboards

    def _extract_dashboard_uids(self, response):
        response_json = json.loads(response.content)
        uid_list = []
        for dashboard in response_json:
            if dashboard['type'] == 'dash-db':
                uid_list.append(dashboard.get('uid'))
        return uid_list

    # Builds list of dashboards from logzio grafana grafana
    def _build_dashboards_list(self) -> list:
        response = requests.get(f'{self._grafana_endpoint}/api/search', headers=self.API_HEADERS)
        dashboards_uids = self._extract_dashboard_uids(response)
        dashboards = []
        for i, uid in enumerate(dashboards_uids):
            response = requests.get(f'{self._grafana_endpoint}/api/dashboards/uid/{uid}', headers=self.API_HEADERS)
            dashboard = response.json()
            dashboards.append(dashboard['dashboard'])
        return dashboards
