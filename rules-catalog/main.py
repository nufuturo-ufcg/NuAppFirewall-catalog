import argparse
import unittest
import os
from utils.csv_helper import read_csv
from managers.rule_manager import create_rules_dict, save_rules_file
from config import consts
import module.log_analysis as mod  

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
                        help='Provide the path to the input txt file of apps that should be blocked.')

    parser.add_argument('-o', '--output', type=str,
                        help='Provide the path for the output catalog (file name without extension).')
    parser.add_argument('-f', '--plist-format', metavar='bin', type=str, default='xml',
                        help='Specify the plist format (default: xml)')
    
    args = parser.parse_args()

    if not (args.input or args.recursive or args.test or args.block):
        parser.error("one of the arguments -i/--input -r/--recursive --test or -b/--block is required")

    if (args.input or args.recursive or args.block) and not args.output:
        parser.error("-o/--output is required when using one of the following arguments: -i/--input, -r/--recursive, -b/--block.")

    if args.block and args.test:
        parser.error("The --test argument cannot be used with -b/--block.")

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


def create_final_rules_dict(network_access_logs_csv_output_path:str, allow_switch:bool):
    """
    Given a path to an intermediate CSV that follows closely the rule format and a
    boolean value to determine if it's going to be a block or allow rule dictionary.

    Args:
        network_access_logs_csv_output_path (str): The path to the intermediate rules' csv.
        allow_switch (bool): Boolean that determines whether the produced rules will be that of block or allow.

    Returns:
        dict: Dictionary of rules.
    """
    
    network_access_logs_dict = read_csv(network_access_logs_csv_output_path)
    rules_dict = create_rules_dict(network_access_logs_dict, allow_switch)

    return rules_dict


def combine_allow_and_block_rules_dict(allow_rule_dict: dict, block_rule_dict: dict):
    """
    Combines two dictionaries containing network access rules, each structured with unique 
    keys that map to lists of rule dictionaries. 
    
    The function merges rules from the 'allow' and 'block' dictionaries into a single combined
    dictionary, where:
      - If a key exists in both dictionaries, it concatenates both lists of rule dictionaries for that key.
      - If a key exists only in one dictionary, it just repeats the key and its list to the combined dictionary.

    Args:
        allow_rule_dict (dict): A dictionary of allow rules, where each key maps to a list containing 
          a single dictionary representing an "allow" action.
        block_rule_dict (dict): A dictionary of block rules, where each key maps to a list containing
          a single dictionary representing a "block" action.
    
    Returns:
        dict: A combined dictionary where each key maps to a list of rule dictionaries from both input
          dictionaries, concatenating the lists when keys are shared.
    """

    combined = {}

    for key in set(allow_rule_dict.keys()).union(block_rule_dict.keys()):
        combined[key] = []

        if key in allow_rule_dict:
            combined[key].extend(allow_rule_dict[key])

        if key in block_rule_dict:
            combined[key].extend(block_rule_dict[key])

    return combined


def main():
    """
    Main function.
    """
    create_data_directory()

    args = parse_arguments()
    if args.test:
        run_tests()
    elif args.block and args.input:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.input
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_sv_file(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        allow_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)

        rules_dict = combine_allow_and_block_rules_dict(allow_rules_dict, block_rules_dict)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)
    elif args.block and args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        allow_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)

        rules_dict = combine_allow_and_block_rules_dict(allow_rules_dict, block_rules_dict)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)
    elif args.block:
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)
    elif args.input:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.input
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_file(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)
    elif args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)

if __name__ == "__main__":
    main()
