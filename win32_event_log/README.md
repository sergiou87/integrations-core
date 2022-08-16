# Agent Check: Windows Event Log

## Overview

The Win 32 event log check watches for Windows Event Logs and forwards them to Datadog. Enable this check to:

- Track system and application events in Datadog.
- Correlate system and application events with the rest of your application.

## Setup

### Installation

The Windows Event Log check is included in the [Datadog Agent][1] package. There is no additional installation required.

### Configuration

Windows Event logs can be collected as either of the following methods. The configuration for them are mutually exclusive.
- As [Datadog Events][15]
- As [Datadog Logs][16]

<!-- xxx tabs xxx -->
<!-- xxx tab "Events" xxx -->
 
#### Event collection

1. Edit the `win32_event_log.d/conf.yaml` in the `conf.d/` folder at the root of your [Agent's configuration directory][2]. See the [sample win32_event_log.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4] to start sending Windows events to Datadog.

**Note**: Events and logs are configured separately. Logs are not configured within each instance. See [log collection](?tab=logs#logcollection), below, for configuring log collection.

<!-- xxz tab xxx -->
<!-- xxx tab "Logs" xxx -->
 
#### Log collection

_Available for Agent versions >6.0_

Log collection is disabled by default in the Datadog Agent; ensure to [activate log collection][14] (e.g. set `logs_enabled: true` in your `datadog.yaml` file) in order to collect Windows Event Logs as Datadog Logs.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

To collect specific Windows Event Logs, add channels to the `conf.d/win32_event_log.d/conf.yaml` file manually, or use the Datadog Agent Manager. See the [Windows Event Logs documentation][13].

To see a list of channels, run the following command in PowerShell:

```powershell
Get-WinEvent -ListLog *
```

To see the most active channels, run the following command in PowerShell:

```powershell
Get-WinEvent -ListLog * | sort RecordCount -Descending
```

This command displays channels in the format `LogMode MaximumSizeInBytes RecordCount LogName`. Example response:

```text
LogMode  MaximumSizeInBytes RecordCount LogName 
Circular 134217728          249896      Security
```

The value under the column `LogName` is the name of the channel. In the above example, the channel name is `Security`.

Depending on collection method, the channel name can be used for the following configuration parameters:
- `log_file`
- `path`
- `channel_path`

<!-- xxx tabs xxx -->
<!-- xxx tab "Events" xxx -->

Add channels to the `path` or `log_file` under the `instances:` section of your `win32_event_log.d/conf.yaml` configuration file. This example shows entries for the `Security` and `<CHANNEL_2>` channels:

```yaml
init_config:
instances:
  - # Legacy mode (default)
    legacy_mode: true
    log_file: Security

  - path: Security 
    legacy_mode: false
    filters: {}

  - path: "<CHANNEL_2>" 
    legacy_mode: false
    filters: {}
```

<!-- xxz tab xxx -->
<!-- xxx tab "Logs" xxx -->

Add channels to the `logs:` section of your `win32_event_log.d/conf.yaml` configuration file. This example shows entries for the `Security` and `<CHANNEL_2>` channels:

```yaml
logs:
  - type: windows_event
    channel_path: Security
    source: windows.events
    service: Windows

  - type: windows_event
    channel_path: "<CHANNEL_2>"
    source: "windows.events"
    service: myservice
```

Set the corresponding `source` parameter to `windows.events` to benefit from the [integration automatic processing pipeline][5].

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

Edit the `<CHANNEL_X>` parameters with the Windows channel name you want to collect events from.

Finally, [restart the Agent][4].

**Note**: For the Security logs channel, add your Datadog Agent user to the `Event Log Readers` user group.

### Filtering events

Use the Windows Event Viewer GUI to list all the event logs available for capture with this integration.

To determine the exact values, set your filters to use the following PowerShell command:

```text
Get-WmiObject -Class Win32_NTLogEvent
```

For example, to see the latest event logged in the `Security` log file, use:

```text
Get-WmiObject -Class Win32_NTLogEvent -Filter "LogFile='Security'" | select -First 1
```

The values listed in the output of the command can be set in `win32_event_log.d/conf.yaml` to capture the same kind of events.

<div class="alert alert-info">
The information given by the  <code> Get-EventLog</code> PowerShell command or the Windows Event ViewerGUI may slightly differ from <code>Get-WmiObject</code>.<br>
Double-check your filters' values with <code>Get-WmiObject</code> if the integration doesn't capture the events you set up.
</div>

1. Configure one or more filters for the event log. A filter allows you to choose what log events you want to get into Datadog.

  Filter on the following properties:

  <!-- xxx tabs xxx -->
  <!-- xxx tab "Events" xxx -->

  Example legacy mode filters:
    - log_file: Application, System, Setup, Security
    - type: Critical, Error, Warning, Information, Audit Success, Audit Failure
    - source_name: Any available source name
    - event_id: Windows EventLog ID

  Example non-legacy mode filters:
    - path: Application, System, Setup, Security
    - type: Critical, Error, Warning, Information, Success Audit, Failure Audit
    - source: Any available source name
    - id: event_id: Windows EventLog ID

  See the [sample win32_event_log.d/conf.yaml][3] for all available filter options for respective modes.

  Some example filters:

  ```yaml
  instances:
    # LEGACY MODE
    # The following captures errors and warnings from SQL Server which
    # puts all events under the MSSQLSERVER source and tag them with #sqlserver.
    - tags:
        - sqlserver
      type:
        - Warning
        - Error
      log_file:
        - Application
      source_name:
        - MSSQLSERVER

    # This instance captures all system errors and tags them with #system.
    - tags:
        - system
      type:
        - Error
      log_file:
        - System
  ```

  ```yaml
  instances:
    # NON-LEGACY MODE
    - path: System
      filters:
        source:
        - Microsoft-Windows-Ntfs
        - Service Control Manager
        type:
        - Error
        - Warning
        - Information
        - Success Audit
        - Failure Audit
        id:
        - 7036
  ```

<!-- xxz tab xxx -->
<!-- xxx tab "Logs" xxx -->

  For each filter, add a log processing rule in the configuration file at `win32_event_log.d/conf.yaml`.

  Some example filters:
  
  ```yaml
    - type: windows_event
      channel_path: Security
      source: windows.events
      service: Windows       
      log_processing_rules:
      - type: include_at_match
        name: relevant_security_events
        pattern: .*(?i)eventid.+(1102|4624|4625|4634|4648|4728|4732|4735|4737|4740|4755|4756)
    - type: windows_event
      channel_path: System
      source: windows.events
      service: Windows       
      log_processing_rules:
      - type: include_at_match
        name: system_errors_and_warnings
        pattern: .*(?i)level.+((?i)(warning|error))
    - type: windows_event
      channel_path: Application
      source: windows.events
      service: Windows       
      log_processing_rules:
      - type: include_at_match
        name: application_errors_and_warnings
        pattern: .*(?i)level.+((?i)(warning|error))
  ```

  Here is an example regex pattern to only collect Windows Events Logs from a certain EventID:

  ```yaml
  logs:
    - type: windows_event
      channel_path: Security
      source: windows.event
      service: Windows
      log_processing_rules:
        - type: include_at_match
          name: include_x01
          pattern: \"value\":\"(101|201|301)\"
  ```

  **Note**: the pattern may vary based on the format of the logs

  For more examples of filtering logs, see the [Advanced Log Collection documentation][12].

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

2. [Restart the Agent][4] using the Agent Manager (or restart the service).

### Validation

<!-- xxx tabs xxx -->
<!-- xxx tab "Events" xxx -->

Check the info page in the Datadog Agent Manager or run the [Agent's `status` subcommand][6] and look for `win32_event_log` under the Checks section. It should display a section similar to the following:

```shell
Checks
======

  [...]

  win32_event_log
  ---------------
      - instance #0 [OK]
      - Collected 0 metrics, 2 events & 1 service check
```

<!-- xxz tab xxx -->
<!-- xxx tab "Logs" xxx -->

Check the info page in the Datadog Agent Manager or run the [Agent's `status` subcommand][6] and look for `win32_event_log` under the Logs Agent section. It should display a section similar to the following:

```shell
Logs Agent
==========

  [...]

  win32_event_log
  ---------------
    - Type: windows_event
      ChannelPath: System
      Status: OK
```

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

## Data Collected

### Metrics

The Win32 Event log check does not include any metrics.

### Events

All Windows events are forwarded to Datadog.

### Service Checks

The Win32 Event log check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][7].

## Further Reading

### Documentation

- [Add event log files to the `Win32_NTLogEvent` WMI class][8]

### Blog

- [Monitoring Windows Server 2012][9]
- [How to collect Windows Server 2012 metrics][10]
- [Monitoring Windows Server 2012 with Datadog][11]

[1]: https://app.datadoghq.com/account/settings#agent/windows
[2]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[3]: https://github.com/DataDog/integrations-core/blob/master/win32_event_log/datadog_checks/win32_event_log/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/logs/processing/pipelines/#integration-pipelines
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://docs.datadoghq.com/help/
[8]: https://docs.datadoghq.com/integrations/guide/add-event-log-files-to-the-win32-ntlogevent-wmi-class/
[9]: https://www.datadoghq.com/blog/monitoring-windows-server-2012
[10]: https://www.datadoghq.com/blog/collect-windows-server-2012-metrics
[11]: https://www.datadoghq.com/blog/windows-server-monitoring
[12]: https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=configurationfile
[13]: https://docs.microsoft.com/en-us/windows/win32/eventlog/event-logging
[14]: https://docs.datadoghq.com/agent/logs/#activate-log-collection
[15]: https://docs.datadoghq.com/events/
[16]: https://docs.datadoghq.com/logs/
