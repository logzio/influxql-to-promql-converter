Grafana Importer
======================
This importer fetches dashboards from grafana API endpoint.

**Configuration Options**:
* ```endpoint``` (required): Grafana API URL.
* ```api_token``` (required): Authorization token for accessing grafana API.

**Example config**:
```
importer:
  grafana:
    endpoint: https://myusername.grafana.net
    api_token: <<grafana api token>>
```