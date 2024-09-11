import argparse
import unittest
import os
from utils.csv_helper import read_csv
from managers.rule_manager import create_rules_dict, save_rules_file
from config import consts
import module.cortex_analysis as mod  

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Namespace: An object holding parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Convert JSON file to output format.')
    parser.add_argument('-o', '--output', metavar='plist', type=str, default='json',
                        help='Specify the output format (default: json)')
    parser.add_argument('-f', '--plist-format', metavar='bin', type=str, default='xml',
                        help='Specify the plist format (default: xml)')
    parser.add_argument('--test', action='store_true', help='Run tests in the test folder')
    return parser.parse_args()

def run_tests():
    """
    Run unit tests in the test folder.
    """
    test_dir = os.path.join(os.path.dirname(__file__), 'test')
    
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(test_dir)
    unittest.TextTestRunner().run(test_suite)

def main():
    """
    Main function.
    """
    args = parse_arguments()
    if args.test:
        run_tests()
    else:
        mod.process_csv(consts.NETWORK_ACCESS_LOGS_CSV_PATH, consts.NETWORK_ACCESS_LOGS_CSV_PATH+"paths.csv")

        network_access_logs_dict = read_csv(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        rules_dict = create_rules_dict(network_access_logs_dict)
        save_rules_file(rules_dict, args.output, args.plist_format)

if __name__ == "__main__":
    main()
