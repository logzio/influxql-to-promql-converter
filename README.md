influxql-to-m3-dashboard-converter
======================

Overview
========

This is our implementation of Grafana® dashboard conversion tooling, which
converts dashboards which use InfluxQL® to M3 (subset) of PromQL™. This is
only offered as reference and is not recommended for usage by anyone as is.

While we have used (slightly different variant of) it in production years,
and still do, correct way of handling this would be to parse InfluxQL
properly instead of having (deeply nested) regexp based handling we do.

Usage
========
1. Clone the repository
2. Edit the configuration file with your settings (see below for example)
3. Run the script:

```
# python3 main.py
```

Configuration
========
The project supports multiple ways to import,process and export dashboards, 
each module is defined in the config file:

```
log_level: # optional default is INFO
datasource: # optional - will be used as the new datasource
importer:      # required - at least 1. 
  grafana:  # grafana api url i.e: https://<<username>>.grafana.net for grafana cloud url
    endpoint:
    api_token:
  folder:
    path:  # relative or full path
processor:
  replace_metrics_names:
    - name: # metric to be replaced
      value: # new metric name
  find_metrics_names:
    metrics_db_endpoint: # currently only m3db is supported     
    metrics_db_header:
      key: 
      value: 
    replace_strategy:
      strategies: [ 'statistic_combination' , 'permutation' ] # optional
      min_match_percent:  # min percent for result match 1-100
      min_filter_percent:  # threshold for combination matching 1-100 
exporter:
  grafana:
    endpoint: # grafana api url i.e: https://<<username>>.grafana.net
    auth_header:
      key:
      value:
  folder:
    path: # relative or full path

```

Example config:
```
datasource: Promql Metrics
log_level: DEBUG
importer:
  grafana:
    endpoint: https://myusername.grafana.net
    api_token: <<grafana_api_token>>
  folder:
    path:  dashboards/influxql
processor:
  replace_metrics_names:
    - name: mem_used
      value: system_memory_usage
  find_metrics_names:
    metrics_db_endpoint: https://api-eu.logz.io/v1/metrics/prometheus/api/v1
    metrics_db_header:
      key: X-API-TOKEN
      value: <<logzio_m3db_prometheus_api_key>>
    replace_strategy:
      strategies: [ 'statistic_combination' , 'permutation' ]
      min_match_percent: 85 
      min_filter_percent: 90 
exporter:
  grafana:
    endpoint:
    auth_header:
      key:
      value:
  folder:
    path: dashboards/promql_converted
```

**Parameters**

| Parameter | Description |
|---|---|
| log_level | **Optional**. Log level to be used during the run of the program. Default: INFO | 
| datasource | **Optional**. Replaces the existing datasource in the dashboard |
| importer | **Required**. At least one input element |
| importer.grafana | **Optional**. Import influxql dashboards from grafana API |
| importer.grafana.endpoint | **Required**. Grafana API URL |
| importer.grafana.token | **Required**. Grafana API token |
| importer.folder | **Optional**: Import influxql dashboards from a folder |
| importer.folder.path | **Required**. Path to the folder which contains influxql dashboards. (Relative or absolute) |
| processor | **Optional**. Processor modules that can transform output |
| processor.replace_metrics_names | **Optional**. A processor that will replace a metric name |
| processor.replace_metrics_names.name | **Required**. The name of the original metric to be replaced |
| processor.replace_metrics_names.value | **Required**. The new metric name |
| processor.find_metrics_names | **Optional**. Processor to find a match between existing and available metrics |
| processor.find_metrics_names.metrics_db_endpoint | **Required**. API endpoint of the metrics db. Currently only m3db is supported. |
| processor.find_metrics_names.metrics_db_endpoint.metrics_db_header.key | **Required**. Metrics db header key to be used when querying the db API. Must be a full header key |
| processor.find_metrics_names.metrics_db_endpoint.metrics_db_header.value | **Required**. Metrics db header value to be used when querying the db API. Must be a full header value, including token |
| processor.find_metrics_names.replace_strategy.strategies | **Required**. Strategies to be used in the processor. Available strategies: permutation,statistic_match |
| processor.find_metrics_names.replace_strategy.min_match_percent | **Required** (for statistic_match strategy). The percent threshold for considering a match between two metrics. |
| processor.find_metrics_names.replace_strategy.min_filter_percent | **Required** (for statistic_match strategy). The percent threshold for performing combination match between two metrics. |
| exporter | **Required**. Exporter module that will export the converted dashboards. | 
| exporter.grafana | **Optional**. Export dashboards using grafana API. |
| exporter.grafana.endpoint | **Required**. grafana API URL. |
| exporter.grafana.auth_header.key | **Required**. Authentication header key. |
| exporter.grafana.auth_header.value | **Required**. Authentication header value. |
| exporter.folder | **Optional**. Export dashboard to a folder. |
| exporter.folder.path | **Required**. Path to the folder in which the dashboards will be exported. (Relative or absolute)|

Contribution
============

License
============
influxql-to-m3-dashboard-converter is licensed under the Apache license,
version 2.0. Full license text is available in the [LICENSE](LICENSE) file.

Please note that the project explicitly does not require a CLA (Contributor
License Agreement) from its contributors.


To report any possible vulnerabilities or other serious issues please see
our [security](SECURITY.md) policy.

Trademarks
==========
InfluxQL® is a trademark owned by InfluxData, which is not affiliated with, and does not endorse, this product.
All product and service names used in this page are for identification purposes only and do not imply endorsement.
