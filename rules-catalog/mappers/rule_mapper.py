import logging
import ast  

def map_network_access_log_to_rule(network_access_log, is_allow) :
    """
    Maps a network access log entry to a rule dictionary.
    
    Parses the 'endpoints' field, validates the log entry, and generates a rule 
    for network access control. If the log entry is invalid or parsing fails, 
    logs an error message.

    Args:
        network_access_log (dict): A dictionary representing a single network access log.
        is_allow (bool): A boolean value that will define if the rules created's nature
          are that of allow or block.

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
        destinations = ast.literal_eval(network_access_log['destinations'])
        if not isinstance(destinations, list):
            raise ValueError("Destinations must be a list.")
    except (ValueError, SyntaxError) as e:
        logging.error(f"Failed to parse endpoints: {e}")
        return None

    value = {
        'action': 'allow' if is_allow else 'block',
        'identifier': network_access_log['identifier'],
        'destinations': destinations
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
    and 'destinations' is a string (later parsed as a list).

    Args:
        row (dict): A dictionary representing a single network access log entry.

    Returns:
        bool: True if the log entry contains all required fields and is valid, 
              False otherwise.
    """
    required_fields = {
        'causality_actor_process_image_path': lambda x: isinstance(x, str) and bool(x.split('/')[-1]),
        'destinations': lambda x: isinstance(x, str),  # Destinations will be validated after conversion
        'identifier': lambda x: isinstance(x, str)
    }

    for field, validator in required_fields.items():
        if field not in row or not validator(row[field]):
            return False

    return True


def validate_rule(rule):
    """
    Validates a generated rule dictionary by checking for required fields.
    
    Ensures the presence of the following fields: 'action', and 'destinations'.
    Additionally, checks that there are no extra fields apart from optional 'csInfo'.
    
    Args:
        rule (dict): A dictionary representing a rule.

    Returns:
        bool: True if the rule contains all required fields and no extra fields, 
              False otherwise.
    """
    required_fields = ['action', 'identifier', 'destinations']
    
    if not all(field in rule for field in required_fields):
        return False
    
    if set(rule.keys()) - set(required_fields) - {'csInfo'}:
        return False

    return True
