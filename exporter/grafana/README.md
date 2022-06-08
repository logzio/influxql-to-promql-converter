Grafana Exporter
======================
This exporter export dashboards to grafana API endpoint.

**Configuration Options**:
* ```endpoint``` (required): Grafana API URL.
* ```auth_header.key``` (required): Authorization header key for accessing grafana API.
* ```auth_header.value``` (required): Authorization header value for accessing grafana API - must contain token.

**Example config**:
```
exporter:
  grafana:
    endpoint: https://myusername.grafana.net
    auth_header: 
      key: Authorization
      value: Bearer <<grafana api token>>
```

**Example config for Logzio API**:
```
exporter:
  grafana:
    endpoint: https://api.logz.io/v1/grafana/api # https://api-<<region>>.logz.io/v1/grafana/api for non us regions
    auth_header:
      key: X-API-TOKEN
      value: <<logzio grafana api token>>
```
