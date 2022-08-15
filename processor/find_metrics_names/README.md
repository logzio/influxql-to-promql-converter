Find metric names processor
======================
This processor searching for a match between metrics in dashboards and in the target db. Currently, only Prometheus is
supported as the target query engine. By default, the processor will look for exact matches between the two metric sources.
If no metrics authentication method is provided, the processor will attempt querying metrics endpoint provided 
with no authentication method.

If specified, permutation and/or statistic matching will be performed. Statistic matching will use the filter percent as
initial filter, before performing more advanced combination matching.
<br>i.e:<br>
db metric: system_cpu_usage, dashboard
metrics: cpu_usage, filter percent: 90, match percent :95.
<br>Match between system_cpu_usage and cpu_usage yield the result of
90, which is within the filter percent given. 
<br>Combination matching will be performed, which will yield a 95 result for
the match between "cpu_usage" and "cpu","usage" combination, which is within the match threshold.
<br> This will result in the switch between cpu_usage ---> system_cpu_usage
<br> The recommended settings for statistic percentage is 95 for filter and match.


**Configuration Options**:

* ```metrics_auth.metrics_db_endpoint``` (required): Metric db API URL.
* ```metrics_auth.metrics_basic_auth.username``` (optional): Metric db username.
* ```metrics_auth.metrics_basic_auth.password``` (optional): Metric db username.
* ```metrics_auth.metrics_oauth_header.key``` (optional): Metric db oauth header key.
* ```metrics_auth.metrics_oauth_header.value``` (optional): Metric db oauth header value.
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
    metrics_auth:
      metrics_db_endpoint: https://<<prometheus_server>>/api/v1
      metrics_basic_auth:
        username:
        password:
      metrics_oauth_header:
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
    metrics_auth:
      metrics_db_endpoint: https://api.logz.io/v1/metrics/prometheus/api/v1 # use https://api-<<region>>.logz.io for non us regions 
      metrics_oauth_header:
        key: X-API-TOKEN
        value: <<logzio-prometheus-api-key>>  # 
    replace_strategy:
      strategies: [ 'statistic_combination' , 'permutation' ]
      min_match_percent: 90 
      min_filter_percent: 95
```