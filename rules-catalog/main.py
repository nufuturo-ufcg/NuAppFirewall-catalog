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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input', type=str,
                        help='Provide the path to the input CSV or TSV logs.')
    group.add_argument('-r', '--recursive', type=str,
                        help='Provide the path to the input directory of CSV or TSV logs.')
    group.add_argument('--test', action='store_true',
                        help='Run tests in the test folder')
    
    parser.add_argument('-o', '--output', type=str,
                        help='Provide the path for the output catalog (file name without extension).')
    parser.add_argument('-f', '--plist-format', metavar='bin', type=str, default='xml',
                        help='Specify the plist format (default: xml)')
    
    args = parser.parse_args()

    if (args.input or args.recursive) and not args.output:
        parser.error("-o/--output is required when using one of the following arguments: -i/--input, -r/--recursive.")

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


def main():
    """
    Main function.
    """
    create_data_directory()

    args = parse_arguments()
    if args.test:
        run_tests()
    elif args.input:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.input
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_file(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        network_access_logs_dict = read_csv(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        rules_dict = create_rules_dict(network_access_logs_dict)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)
    elif args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        network_access_logs_dict = read_csv(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        rules_dict = create_rules_dict(network_access_logs_dict)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.plist_format)

if __name__ == "__main__":
    main()
