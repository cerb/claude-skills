---
id: "docs-plugins-cerberusweb-datacenter-sensors"
title: "Plugin: Sensors"
url: "https://cerb.ai/docs/plugins/cerberusweb.datacenter.sensors/"
summary: "This page provides detailed information about the 'Sensors' plugin for Cerb, developed by Webgroup Media, LLC. The plugin introduces flexible Sensor objects designed for network and server monitoring and operational intelligence. It includes various extensions such as Bot Event, Page Section, Page Type, Record Type, Rest API Controller, Scheduled Job, Sensor Type, and Workspace Widget Datasource. Each extension is associated with specific functionalities, like recording custom behavior on sensors, managing sensor page sections, and handling different sensor types such as External, HTTP, and Port. The plugin is structured to enhance monitoring capabilities within the Cerb environment."
tags: ["docs"]
---
| **Name:** | Sensors |
| **Identifier (ID):** | cerberusweb.datacenter.sensors |
| **Author:** | Webgroup Media, LLC. |
| **Path:** | storage/plugins/cerberusweb.datacenter.sensors/ |
| **Image:** |  |

This plugin adds flexible Sensor objects that can be used for network and server monitoring, operational intelligence, etc.

- Extensions
  - Bot Event
  - Page Section
  - Page Type
  - Record Type
  - Rest API Controller
  - Scheduled Job
  - Sensor Type
  - Workspace Widget Datasource

# Extensions

### Bot Event

| Record custom behavior on sensor | `event.macro.sensor` |

### Page Section

| Sensor Page Section | `cerberusweb.profiles.sensor` |

### Page Type

| Sensors Page | `cerberusweb.datacenter.sensors.page` |

### Record Type

| Sensor | `cerberusweb.contexts.datacenter.sensor` |

### Rest API Controller

| Sensors | `cerberusweb.datacenter.sensors.rest` |

### Scheduled Job

| Network and service monitoring | `cerberusweb.datacenter.sensors.cron` |

### Sensor Type

| External | `cerberusweb.datacenter.sensor.external` |
| HTTP | `cerberusweb.datacenter.sensor.http` |
| Port | `cerberusweb.datacenter.sensor.port` |

### Workspace Widget Datasource

| **Sensor** | `cerberusweb.datacenter.sensor.widget.datasource` |

\< Plugins

