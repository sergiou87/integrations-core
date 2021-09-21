# Etcd Integration

![Etcd Dashboard][1]

## Overview

Collect Etcd metrics to:

- Monitor the health of your Etcd cluster.
- Know when host configurations may be out of sync.
- Correlate the performance of Etcd with the rest of your applications.

## Setup

### Installation

The Etcd check is included in the [Datadog Agent][2] package, so you don't need to install anything else on your Etcd instance(s).

### Configuration

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

To configure this check for an Agent running on a host:

##### Metric collection

1. Edit the `etcd.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start collecting your Etcd performance data. See the [sample etcd.d/conf.yaml][4] for all available configuration options.
2. [Restart the Agent][5]

##### Log collection

{{< site-region region="us3" >}}
**Log collection is not supported for this site.**
{{< /site-region >}}

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

    ```yaml
    logs_enabled: true
    ```

2. Uncomment and edit this configuration block at the bottom of your `etcd.d/conf.yaml`:

    ```yaml
    logs:
      - type: file
        path: "<LOG_FILE_PATH>"
        source: etcd
        service: "<SERVICE_NAME>"
    ```

    Change the `path` and `service` parameter values based on your environment. See the [sample etcd.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

#### Containerized

For containerized environments, see the [Autodiscovery Integration Templates][6] for guidance on applying the parameters below.

##### Metric collection

| Parameter            | Value                                                |
| -------------------- | ---------------------------------------------------- |
| `<INTEGRATION_NAME>` | `etcd`                                               |
| `<INIT_CONFIG>`      | blank or `{}`                                        |
| `<INSTANCE_CONFIG>`  | `{"prometheus_url": "http://%%host%%:2379/metrics"}` |

##### Log collection

{{< site-region region="us3" >}}
**Log collection is not supported for this site.**
{{< /site-region >}}

Collecting logs is disabled by default in the Datadog Agent. To enable it, see [Kubernetes log collection][11].

| Parameter      | Value                                             |
| -------------- | ------------------------------------------------- |
| `<LOG_CONFIG>` | `{"source": "etcd", "service": "<SERVICE_NAME>"}` |

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Validation

[Run the Agent's `status` subcommand][7] and look for `etcd` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

Etcd metrics are tagged with `etcd_state:leader` or `etcd_state:follower`, depending on the node status, so you can easily aggregate metrics by status.

### Events

The Etcd check does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].

## Further Reading

To get a better idea of how (or why) to integrate Etcd with Datadog, check out our [blog post][10] about it.

[1]: https://raw.githubusercontent.com/DataDog/integrations-core/master/etcd/images/etcd_dashboard.png
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-core/blob/master/etcd/datadog_checks/etcd/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-core/blob/master/etcd/metadata.csv
[9]: https://docs.datadoghq.com/help/
[10]: https://www.datadoghq.com/blog/monitor-etcd-performance
[11]: https://docs.datadoghq.com/agent/kubernetes/log/
[12]: https://github.com/DataDog/integrations-core/blob/master/etcd/assets/service_checks.json