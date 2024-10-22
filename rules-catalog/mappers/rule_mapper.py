import logging
import ast  

def map_network_access_log_to_rule(network_access_log):
    """
    Maps a network access log entry to a rule dictionary.
    
    Parses the 'endpoints' field, validates the log entry, and generates a rule 
    for network access control. If the log entry is invalid or parsing fails, 
    logs an error message.

    Args:
        network_access_log (dict): A dictionary representing a single network access log.

    Returns:
        dict or None: A dictionary containing the generated rule if the log is valid, 
                      or None if an error occurs during processing or validation.
    """
    if not validate_network_access_log(network_access_log):
        logging.error("Invalid network access log. Please check the required fields. Rule will not be generated.")
        return None
    
    rule = {}

    key = network_access_log['causality_actor_process_image_path']
    
    try:
        endpoints = ast.literal_eval(network_access_log['endpoints'])
        domains = ast.literal_eval(network_access_log['domains'])
        if not isinstance(endpoints, list):
            raise ValueError("Endpoints must be a list.")
        elif not isinstance(domains, list):
            raise ValueError("Domains must be a list.")
    except (ValueError, SyntaxError) as e:
        logging.error(f"Failed to parse endpoints: {e}")
        return None

    value = {
        'key': key,
        'action': 'allow',
        'path': key,
        'endpoints': endpoints,  
        'domains': domains
    }

    rule[key] = {
        key: [value]
    }
    
    if not validate_rule(value):
        logging.error("Invalid rule generated. Please check the required fields.")
        return None
    
    return rule


def validate_network_access_log(row):
    """
    Validates a network access log entry by checking for required fields and their validity.
    
    The required fields are 'causality_actor_process_image_path' and 'endpoints'.
    The validation ensures that 'causality_actor_process_image_path' is a string
    and 'endpoints' is a string (later parsed as a list).

    Args:
        row (dict): A dictionary representing a single network access log entry.

    Returns:
        bool: True if the log entry contains all required fields and is valid, 
              False otherwise.
    """
    required_fields = {
        'causality_actor_process_image_path': lambda x: isinstance(x, str) and bool(x.split('/')[-1]),
        'endpoints': lambda x: isinstance(x, str)  # Endpoints will be validated after conversion
    }

    for field, validator in required_fields.items():
        if field not in row or not validator(row[field]):
            return False

    return True


def validate_rule(rule):
    """
    Validates a generated rule dictionary by checking for required fields.
    
    Ensures the presence of the following fields: 'key', 'action', 'path', 'endpoints', and 'domains'.
    Additionally, checks that there are no extra fields apart from optional 'csInfo'.
    
    Args:
        rule (dict): A dictionary representing a rule.

    Returns:
        bool: True if the rule contains all required fields and no extra fields, 
              False otherwise.
    """
    required_fields = ['key', 'action', 'path', 'endpoints', 'domains']
    
    if not all(field in rule for field in required_fields):
        return False
    
    if set(rule.keys()) - set(required_fields) - {'csInfo'}:
        return False

    return True
