from mappers.rule_mapper import map_network_access_log_to_rule
from utils.json_helper import write_json
from utils.plist_helper import write_plist
from config import consts
import plistlib

def create_rules_dict(network_access_logs_dict, is_allow):
    """
    Maps dictionary of network access logs to dictionary of rules. (See /rules-catalog/README.md to understand details.)
    If existing key already exists, list is appended, otherwise a new entry is created. 

    Args:
    log_dict (list): Dictionary representing the network access logs.
    
    Returns:
    list: Dictionary of rules.
    """        
    rules_dict = {}
    for log_dict in network_access_logs_dict:
        rule_dict = map_network_access_log_to_rule(log_dict, is_allow)
        if rule_dict is not None:
            for key, value in rule_dict.items():
                if key in rules_dict:
                    rules_dict[key].extend(value[key])
                else:
                    rules_dict[key] = value[key]
    return rules_dict

def save_rules_file(rules_dict, output_path, output_format):
    """
    Write output data to file in {output_path}.

    Args:
        rules_dict (dict): Dictionary containing rules.
        output_path (str): String referring as destination path.
        output_format (str): The output format. Defaults to 'json'. Can be 'xml' for XML plist or 'bin' for binary plist.
    """
    if output_format == 'xml':
        write_plist(rules_dict, output_path + consts.EXTENSION_PLIST, plistlib.FMT_XML)
    elif output_format == 'bin':
        write_plist(rules_dict, output_path + consts.EXTENSION_PLIST, plistlib.FMT_BINARY)
    else:
        write_json(rules_dict, output_path + consts.EXTENSION_JSON) 