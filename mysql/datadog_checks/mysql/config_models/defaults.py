# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from datadog_checks.base.utils.models.fields import get_default_field_value


def shared_global_custom_queries(field, value):
    return get_default_field_value(field, value)


def shared_service(field, value):
    return get_default_field_value(field, value)


def instance_additional_status(field, value):
    return get_default_field_value(field, value)


def instance_additional_variable(field, value):
    return get_default_field_value(field, value)


def instance_aws(field, value):
    return get_default_field_value(field, value)


def instance_azure(field, value):
    return get_default_field_value(field, value)


def instance_charset(field, value):
    return get_default_field_value(field, value)


def instance_connect_timeout(field, value):
    return 10


def instance_custom_queries(field, value):
    return get_default_field_value(field, value)


def instance_dbm(field, value):
    return False


def instance_defaults_file(field, value):
    return get_default_field_value(field, value)


def instance_disable_generic_tags(field, value):
    return False


def instance_empty_default_hostname(field, value):
    return False


def instance_gcp(field, value):
    return get_default_field_value(field, value)


def instance_host(field, value):
    return get_default_field_value(field, value)


def instance_log_unobfuscated_plans(field, value):
    return False


def instance_log_unobfuscated_queries(field, value):
    return False


def instance_max_custom_queries(field, value):
    return 20


def instance_metric_patterns(field, value):
    return get_default_field_value(field, value)


def instance_min_collection_interval(field, value):
    return 15


def instance_obfuscator_options(field, value):
    return get_default_field_value(field, value)


def instance_only_custom_queries(field, value):
    return False


def instance_options(field, value):
    return get_default_field_value(field, value)


def instance_password(field, value):
    return get_default_field_value(field, value)


def instance_port(field, value):
    return 3306


def instance_queries(field, value):
    return get_default_field_value(field, value)


def instance_query_activity(field, value):
    return get_default_field_value(field, value)


def instance_query_metrics(field, value):
    return get_default_field_value(field, value)


def instance_query_samples(field, value):
    return get_default_field_value(field, value)


def instance_reported_hostname(field, value):
    return get_default_field_value(field, value)


def instance_service(field, value):
    return get_default_field_value(field, value)


def instance_sock(field, value):
    return get_default_field_value(field, value)


def instance_ssl(field, value):
    return get_default_field_value(field, value)


def instance_tags(field, value):
    return get_default_field_value(field, value)


def instance_use_global_custom_queries(field, value):
    return 'true'


def instance_username(field, value):
    return get_default_field_value(field, value)
