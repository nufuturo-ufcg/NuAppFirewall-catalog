# Catalog Rule Nu App Firewall

## Overview

This document describes the mapping between properties of NuAppFirewall and Cortex XDR. NuAppRule represents the target entity, while Cortex XDR represents the source entities. No Mapping (NM) means that there is no equivalente method for this property and some default value might be used.

### Property Mapping

| NuAppRule               | Cortex XDR Log                              | Mandatory |
|-------------------------|---------------------------------------------|-----------|
| **key**                 | causality_actor_process_image_path                           | Yes       |
| **action**              | (NM) 'allow', 'block', or 'nolog' (defined according to rules) | Yes       |
| **destinations**           | action_remote_ip and action_remote_port or dst_action_external_hostname and action_remote_port | Yes       |

### Property Descriptions

1. **key**
   - **Description**: Represents the unique identifier for the rule, derived from the path of the process image.
   - **Usage**: Used as the primary identifier to associate a specific application or process with the rule.

2. **action**
   - **Description**: Defines the action that the rule will enforce, which can be 'allow', 'block', or 'nolog'.
   - **Usage**: Specifies the enforcement behavior of the rule on the network traffic.

3. **destinations**
   - **Description**: Lists the network pairs of IP addresses or hostnames and ports involved.
   - **Usage**: Specifies the exact destinations for the network traffic, including both the target IP addresses or hostnames and their associated ports. These define where the traffic is intended to be delivered or received within the network.