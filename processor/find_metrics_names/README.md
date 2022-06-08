Find metric names processor
======================
This processor searching for a match between metrics in dashboards and in the target db. Currently, only m3db is
supported as the target db. By default, the processor will look for exact matches between the two metric sources. If
specified, permutation and/or statistic matching will be performed. Statistic matching will use the filter percent as
initial filter, before performing more advanced combination matching.
<br>i.e:<br>
db metric: system_cpu_usage, dashboard
metrics: cpu_usage, filter percent: 90, match percent :95.
<br>Match between system_cpu_usage and cpu_usage yield the result of
90, which is within the filter percent given. 
<br>Combination matching will be performed, which will yield a 95 result for
the match between "cpu_usage" and "cpu","usage" combination, which is within the match threshold.
<br> This will result in the switch between cpu_usage ---> system_cpu_usage

**Configuration Options**:

* ```metrics_db_endpoint``` (required): Metric db API URL.
* ```metrics_db_header.key``` (required): Metric db auth header key.
* ```metrics_db_header.value``` (required): Metric db auth header value.
* ```replace_strategy.strategies``` (required): Strategies to be used in the processor. Available strategies:
  permutation,statistic_match.
* ```replace_strategy.min_match_percent``` (required): The percent threshold for considering a match between two
  metrics.
* ```replace_strategy.min_filter_percent``` (required): The percent threshold for performing combination match between
  two metrics.

**Example config**:

```
processor:
  find_metrics_names:
    metrics_db_endpoint: https://<<prometheus_server>>/api/v1
    metrics_db_header:
      key: 
      value: 
    replace_strategy:
      strategies: [ 'statistic_combination' , 'permutation' ]
      min_match_percent: 90 
      min_filter_percent: 91
```

**Example config for Logzio API:**

```
processor:
  find_metrics_names:
    metrics_db_endpoint: https://api.logz.io/v1/metrics/prometheus/api/v1 # use https://api-<<region>>.logz.io for non us regions 
    metrics_db_header:
      key: X-API-TOKEN
      value: <<logzio-m3db-prometheus-api-key>>  # 
    replace_strategy:
      strategies: [ 'statistic_combination' , 'permutation' ]
      min_match_percent: 90 
      min_filter_percent: 95
```