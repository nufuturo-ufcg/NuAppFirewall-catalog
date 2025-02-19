import argparse
import os
import unittest
from utils.csv_helper import read_csv
from managers.rule_manager import create_rules_dict

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Namespace: An object holding parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process network access logs and generate rules.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', type=str,
                        help='Provide the path to the input CSV or TSV logs.')
    group.add_argument('-r', '--recursive', type=str,
                        help='Provide the path to the input directory of CSV or TSV logs.')
    group.add_argument('--test', action='store_true',
                        help='Run tests in the test folder')
    
    parser.add_argument('-b', '--block', type=str,
                        help='Provide the path to the input csv file of apps that should be blocked.')
    parser.add_argument('--port-blocking', type=str,
                        help='Provide the path to the input txt file of ports that should be blocked.')

    parser.add_argument('-o', '--output', type=str,
                        help='Provide the path for the output catalog (file name without extension).')
    parser.add_argument('--simplified', action='store_true',
                        help='Simplifies destinations to (endpoint, "any") if an endpoint has >99 occurrences for a single app.')
    
    output_format_group = parser.add_mutually_exclusive_group()
    output_format_group.add_argument('--plist', action='store_true',
                                    help='Output rules in binary plist format.')
    output_format_group.add_argument('--plist-xml', action='store_true',
                                    help='Output rules in XML plist format.')
    
    args = parser.parse_args()

    if not (args.input or args.recursive or args.test or args.block or args.port_blocking):
        parser.error("one of the arguments -i/--input -r/--recursive --test -b/--block or --port-blocking is required")

    if (args.input or args.recursive or args.block or args.port_blocking) and not args.output:
        parser.error("-o/--output is required when using one of the following arguments: -i/--input, -r/--recursive, -b/--block, --port-blocking.")

    if (args.block or args.port_blocking) and args.test:
        parser.error("--test argument cannot be used with -b/--block or --port-blocking.")

    if args.simplified and args.test:
        parser.error("--test argument cannot be used with --simplified.")

    if (args.plist or args.plist_xml) and args.test:
        parser.error("--test argument cannot be used with --plist or --plist-xml.")

    if args.plist:
        args.format = 'bin'
    elif args.plist_xml:
        args.format = 'xml'
    else:
        args.format = 'json'

    return args


def run_tests():
    """
    Run unit tests in the test folder.
    """
    test_dir = os.path.join(os.path.dirname(__file__), 'test')
    
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(test_dir)
    unittest.TextTestRunner().run(test_suite)


def create_data_directory():
    """
    Create a directory named 'data' if it does not exist.
    """
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def create_final_rules_dict(network_access_logs_csv_output_path: str, is_allow: bool):
    """
    Given a path to an intermediate CSV that follows closely the rule format and a
    boolean value to determine if it's going to be a block or allow rule dictionary.

    Args:
        network_access_logs_csv_output_path (str): The path to the intermediate rules' csv.
        is_allow (bool): Boolean that determines whether the produced rules will be that of block or allow.

    Returns:
        dict: Dictionary of rules.
    """
    
    network_access_logs_dict = read_csv(network_access_logs_csv_output_path)
    rules_dict = create_rules_dict(network_access_logs_dict, is_allow)

    return rules_dict


def combine_allow_and_block_rules_dict(allow_rules_dict: dict, block_rules_dict: dict):
    """
    Combines two dictionaries containing network access rules, each structured with unique 
    keys that map to lists of rule dictionaries. 
    
    The function merges rules from the 'allow' and 'block' dictionaries into a single combined
    dictionary, where:
      - If a key exists in both dictionaries, it concatenates both lists of rule dictionaries for that key.
      - If a key exists only in one dictionary, it just repeats the key and its list to the combined dictionary.

    Args:
        allow_rules_dict (dict): A dictionary of allow rules, where each key maps to a list containing 
          a single dictionary representing an "allow" action.
        block_rules_dict (dict): A dictionary of block rules, where each key maps to a list containing
          a single dictionary representing a "block" action.
    
    Returns:
        dict: A combined dictionary where each key maps to a list of rule dictionaries from both input
          dictionaries, concatenating the lists when keys are shared.
    """

    combined = {}

    for key in set(allow_rules_dict.keys()).union(block_rules_dict.keys()):
        combined[key] = []

        if key in allow_rules_dict:
            combined[key].extend(allow_rules_dict[key])

        if key in block_rules_dict:
            combined[key].extend(block_rules_dict[key])

    return combined


def remove_conflicting_rules(rules_dict):
    """
    Removes conflicting rules from a dictionary of rules. A conflict occurs when:
      - A rule with a specific identifier has an action of "block".
      - Another rule with the same identifier has an action of "allow".

    In such cases, the "allow" rule is considered conflicting and is removed from the dictionary.

    Args:
        rules_dict (dict): A dictionary of rules:

    Returns:
        dict: The modified dictionary with conflicting "allow" rules removed.
    """
    block_identifiers = set()
    keys_to_remove = []

    for path, rules in list(rules_dict.items()):
        rule = rules[0]
        identifier = rule['identifier']

        if identifier != 'unknown' and rule['action'] == 'block':
            block_identifiers.add(identifier)
    
    for path, rules in list(rules_dict.items()):
        rule = rules[0]
        identifier = rule["identifier"]

        if identifier in block_identifiers and rule['action'] == 'allow':
            keys_to_remove.append(path)

    for key in keys_to_remove:
        if key in rules_dict:
            del rules_dict[key]

    return rules_dict
