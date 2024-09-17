# Catalog Rule Nu App Firewall

## Overview

This document describes the mapping between properties of NuAppFirewall and Cortex XDR. NuAppRule represents the target entity, while Cortex XDR represents the source entities. No Mapping (NM) means that there is no equivalente method for this property and some default value might be used.

### Property Mapping

| NuAppRule               | Cortex XDR Log                              | Mandatory |
|-------------------------|---------------------------------------------|-----------|
| **key**                 | causality_actor_process_image_path                           | Yes       |
| **action**              | (NM) 'allow', 'block', or 'nolog' (defined according to rules) | Yes       |
| **path**         | causality_actor_process_image_path | Yes       |
| **endpoints**           | action_remote_ip and dst_action_external_hostname | Yes       |
| **direction**           | (NM) 'outgoing' or 'ingoing' (defined according to rules)                    | Yes       |

### Property Descriptions

1. **key**
   - **Description**: Represents the unique identifier for the rule, derived from the path of the process image.
   - **Usage**: Used as the primary identifier to associate a specific application or process with the rule.

2. **action**
   - **Description**: Defines the action that the rule will enforce, which can be 'allow', 'block', or 'nolog'.
   - **Usage**: Specifies the enforcement behavior of the rule on the network traffic.

3. **path**
   - **Description**: Indicates the location or path of the application or process image that the rule is associated with.
   - **Usage**: Used to pinpoint the exact location of the application or process being regulated by the rule.

4. **endpoints**
   - **Description**: Lists the network endpoints involved, including IP addresses and hostnames.
   - **Usage**: Defines the specific network locations that the rule applies to, such as remote IPs or external hostnames involved in the network traffic.

5. **direction**
   - **Description**: Specifies the direction of the traffic flow that the rule applies to, either 'outgoing' or 'ingoing'.
   - **Usage**: Determines whether the rule applies to outbound (outgoing) or inbound (ingoing) network traffic.


