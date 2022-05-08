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
1. Fork the repository
2. Place all the influxql dashboards in the "dashboards" folder.
3. Run the script:

```
# python3 influxql_to_m3_dashboard_converter.py
```

Each parsed file will have the same name with a "_promql" suffix.

License
============
influxql-to-m3-dashboard-converter is licensed under the Apache license,
version 2.0. Full license text is available in the [LICENSE](LICENSE) file.

Please note that the project explicitly does not require a CLA (Contributor
License Agreement) from its contributors.

Contact
============
Bug reports and patches are not welcome; better implementation is very
welcome though, please let us know if you find something that does this
better than this one does.

To report any possible vulnerabilities or other serious issues please see
our [security](SECURITY.md) policy.

Trademarks
==========
InfluxQL® is a trademark owned by InfluxData, which is not affiliated with, and does not endorse, this product.
All product and service names used in this page are for identification purposes only and do not imply endorsement.
