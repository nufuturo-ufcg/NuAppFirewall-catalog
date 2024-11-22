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

def save_rules_file(rules_dict, output_format, plist_format):
    """
    Write output data to file in {output_format}.

    Args:
        rules_dict (dict): Dictionary containing rules.
        output_format (str): Output format ('json' or 'plist').
    """
    if output_format == 'plist':
        output_plist_format = plistlib.FMT_XML
        if plist_format == 'bin':
            output_plist_format = plistlib.FMT_BINARY
        write_plist(rules_dict, consts.RULES_FILE_PATH + consts.EXTENSION_PLIST, output_plist_format)
    else:
        write_json(rules_dict, consts.RULES_FILE_PATH + consts.EXTENSION_JSON)

