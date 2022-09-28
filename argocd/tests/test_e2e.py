# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import pytest

from datadog_checks.base.constants import ServiceCheck

from .common import API_SERVER_METRICS, APP_CONTROLLER_METRICS, NOT_EXPOSED_METRICS, REPO_SERVER_METRICS


@pytest.mark.e2e
def test_e2e_openmetrics_v1(dd_agent_check):
    aggregator = dd_agent_check(rate=True)
    metrics = APP_CONTROLLER_METRICS + API_SERVER_METRICS + REPO_SERVER_METRICS

    aggregator.assert_service_check('argocd.api_server.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_service_check('argocd.repo_server.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_service_check('argocd.app_controller.openmetrics.health', ServiceCheck.OK)

    for metric in metrics:
        if metric in NOT_EXPOSED_METRICS:
            aggregator.assert_metric(metric, at_least=0)
        else:
            aggregator.assert_metric(metric)
