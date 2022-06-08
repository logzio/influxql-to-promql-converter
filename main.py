import importlib
import logging
import time
import yaml

from converter.influxql_to_m3_dashboard_converter import InfluxQLToM3DashboardConverter, ConvertError

logger = logging.getLogger(__name__)


def get_log_level_descriptor(log_level) -> int:
    if log_level:
        return getattr(logging, log_level)
    return logging.INFO


def extend_module_name(module_name: str, module_type: str) -> str:
    return module_type + "." + module_name + "." + module_name + "_" + module_type


def create_class_name(module: str, module_type: str) -> str:
    import re
    capitalized_module_name = re.sub("(^|[_])\s*([a-zA-Z])", lambda p: p.group(0).upper(), module)
    return capitalized_module_name.replace("_", "") + module_type.capitalize()


# TODO improve logic
def is_influx_dashboard(dashboard_item):
    expr_exists = False  # promql dashboard will have an expr element in targets
    try:
        for panel in dashboard_item['panels']:
            if panel.get('targets'):
                for target in panel['targets']:
                    if target.get('measurement'):
                        return True
                    elif target.get('expr'):
                        expr_exists = True
            elif panel.get('panels'):
                for inner_panel in panel['panels']:
                    if inner_panel.get('targets'):
                        for target in inner_panel['targets']:
                            if target.get('measurement'):
                                return True
                            elif target.get('expr'):
                                expr_exists = True
    except KeyError:
        logger.warning(f"Dashboard {dashboard_item['title']} is not a valid influxdb dashboard, skipping.")
        return False
    return expr_exists


def run():
    start_time = time.time()
    modules = [list(), list(), list()]  # [0] - inputs , [1] - processors , [2] - exporters
    module_names = ['importer', 'processor', 'exporter']
    dashboards = []
    report = {}
    invalid_dashboards = []
    # v = Schema(json.load(open('config_schema.json', 'r')))
    config = build_module_list_from_config(module_names, modules)
    logging.getLogger(__name__).setLevel(level=get_log_level_descriptor(config.get('log_level')))

    import_dashboards(dashboards, modules[0])
    converter = InfluxQLToM3DashboardConverter(replacement_datasource=config.get('datasource'),
                                               log_level=get_log_level_descriptor(config.get('log_level')))
    influx_dashboards = []
    convert_dashboards(converter, dashboards, influx_dashboards, invalid_dashboards)
    metric_to_objects = converter.metric_to_objects
    metric_to_objects = process_dashboards(metric_to_objects, modules[1], report)
    export_dashboards(influx_dashboards, modules[2])
    logger.info(f"Finished converting {len(influx_dashboards)} dashboards")
    create_report(invalid_dashboards, metric_to_objects, modules[1], report)
    logger.info(f"Finished running in --- {(time.time() - start_time)} seconds ---  ")


def build_module_list_from_config(module_names, modules) -> dict:
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
        # v.validate(config)
        for index in range(0, 3):
            if config.get(module_names[index]):
                for module in [_module for _module in config[module_names[index]] if config.get(module_names[index])]:
                    module_class = getattr(
                        importlib.import_module(name=extend_module_name(module, module_names[index])),
                        create_class_name(module, module_names[index]))
                    # Instantiate the class (pass arguments to the constructor, if needed)
                    try:
                        module_instance = module_class(config[module_names[index]][module],
                                                       get_log_level_descriptor(config.get('log_level')))
                        modules[index].append(module_instance)
                    except (KeyError, ValueError) as e:
                        logger.error(f"Error validating config for module: {module} with error: {str(e)}, skipping")
    return config


def import_dashboards(dashboards, inputs):
    for input in inputs:
        logger.info(f"Starting to fetch dashboards from importer: {input}")
        dashboards.extend(input.fetch_dashboards())


def export_dashboards(influx_dashboards, exporters):
    for exporter in exporters:
        logger.info(f"Exporting dashboards with exporter: {exporter}")
        exporter.export_dashboards(influx_dashboards)


def add_report_extended_info(report):
    enchanced_report = {}
    if len(report) > 0:
        for dashboard, values in report.items():
            if values.get("unreplaced_metrics"):
                values[
                    "Unable to find any match for the following metrics. Please check the dashboard manually"] = values.pop(
                    "unreplaced_metrics")
            enchanced_report[f"Dashboard name: {dashboard}"] = report[dashboard]
    return enchanced_report


def create_report(invalid_dashboards, metric_to_objects, processors, report):
    logger.info("Building result report")
    if len(processors) > 0 and len(metric_to_objects) > 0:  # rebuild unreplaced metrics per dashboard
        add_unreplaced_metrics_to_report(metric_to_objects, report)
    report = add_report_extended_info(report)
    report['skipped dashboards'] = invalid_dashboards
    if len(report) > 0:
        with open('result_report.yml', 'w') as outfile:
            yaml.dump(report, outfile, default_flow_style=False)
    logger.info("Finished building result report: result_report.yaml")


def process_dashboards(metric_to_objects, processors, report) -> dict:
    for processor in processors:
        logger.info(f"Processing dashboards with processor: {processor}")
        metric_to_objects = processor.process(metric_to_objects)
        for dashboard_key, processor_report in processor.get_json_report().items():
            if not report.get(dashboard_key):
                report[dashboard_key] = processor_report
            else:
                report[dashboard_key] = report[dashboard_key] | processor_report
    return metric_to_objects


def convert_dashboards(converter, dashboards, influx_dashboards, invalid_dashboards):
    for dashboard in dashboards:
        if is_influx_dashboard(dashboard):
            logger.info(f"Starting dashboards conversion")
            try:
                converter.convert_dashboard(dashboard)
                influx_dashboards.append(dashboard)
            except ConvertError as e:
                logger.error(
                    f"Error converting dashboard {dashboard['title']} with error: {str(e)}. skipping conversion.")
                invalid_dashboards.append(dashboard['title'])
        else:
            invalid_dashboards.append(dashboard['title'])


def add_unreplaced_metrics_to_report(metric_to_objects, report):
    dashboard_metrics = dict()
    unreplaced_metrics_report = []
    for metric, dash_dict in metric_to_objects.items():
        for dashboard, panel in dash_dict.items():
            if not dashboard_metrics.get(dashboard):
                dashboard_metrics[dashboard] = []
            dashboard_metrics[dashboard].append(metric)

    for dashboard, metrics in dashboard_metrics.items():
        unreplaced_metrics_report.append({dashboard: {"unreplaced_metrics": metrics}})
    for dashboard_to_metrics in unreplaced_metrics_report:
        for dashboard, metrics in dashboard_to_metrics.items():
            if not report.get(dashboard):
                report[dashboard] = dashboard_to_metrics.get(dashboard)
            else:
                report[dashboard] = report[dashboard] | dashboard_to_metrics[dashboard]


if __name__ == '__main__':
    run()
