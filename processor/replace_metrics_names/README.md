Replace metric names processor
======================
This processor replaces a metric name by another.

**Configuration Options**:
* ```name``` (required): Existing metric name to be replaced.
* ```value``` (required): New metric name.

**Example config**:
```
processor:
  replace_metrics_names:
    - name: <<existing metric name>>
      value: <<new metric name>>
```