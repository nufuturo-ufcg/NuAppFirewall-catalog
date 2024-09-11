import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def map_network_access_log_to_rule(network_access_log): 
    
    if not validate_network_access_log(network_access_log):
        logging.error("Invalid network access log. Please check the required fields. Rule will not be generated.")
        return None
    
    rule = {}

    key = network_access_log['causality_actor_process_image_path']
    
    value = {
    'key': key,
    'action': 'allow',
    'appLocation': key,
    'endpoints': network_access_log['endpoints'], 
    'direction': 'outgoing'
    }

    rule[key] = {
        key: [value]
    }
    
    if not validate_rule(value):
        logging.error("Invalid rule generated. Please check the required fields.")
        return None
    return rule

def validate_network_access_log(row):
    required_fields = {
        'causality_actor_process_image_path': lambda x: isinstance(x, str) and bool(x.split('/')[-1]),
        'endpoints': lambda x: isinstance(x, str)
    }

    for field, validator in required_fields.items():
        if field not in row or not validator(row[field]):
            return False

    return True
    
def validate_rule(rule):
    required_fields = ['key', 'action', 'appLocation', 'endpoints', 'direction']
    
    # Check if all required fields are present
    if not all(field in rule for field in required_fields):
        return False
    
    # Check if any extra fields are present
    if set(rule.keys()) - set(required_fields) - {'csInfo'}:
        return False

    return True
