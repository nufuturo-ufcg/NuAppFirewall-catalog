from config import consts
from managers.rule_manager import save_rules_file
import module.cortex_analysis as mod
from utils.main_helper import *

def main():
    """
    Main function.
    """
    create_data_directory()

    args = parse_arguments()
    if args.test:
        run_tests()
    elif args.block and args.port_blocking and args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.NETWORK_BLOCK_PORTS_PATH = args.port_blocking
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        allow_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)

        mod.process_block_ports(consts.NETWORK_BLOCK_PORTS_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_ports_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        rules_dict = remove_conflicting_rules(combine_allow_and_block_rules_dict(allow_rules_dict, block_rules_dict))
        
        rules_dict = combine_allow_and_block_rules_dict(rules_dict, block_ports_dict)

        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.block and args.port_blocking:
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.NETWORK_BLOCK_PORTS_PATH = args.port_blocking
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_block_ports(consts.NETWORK_BLOCK_PORTS_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_ports_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        rules_dict = combine_allow_and_block_rules_dict(block_rules_dict, block_ports_dict)

        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.port_blocking:
        consts.NETWORK_BLOCK_PORTS_PATH = args.port_blocking
        consts.RULES_FILE_PATH = args.output

        mod.process_block_ports(consts.NETWORK_BLOCK_PORTS_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_ports_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        save_rules_file(block_ports_dict, consts.RULES_FILE_PATH, args.format)
    elif args.block and args.input:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.input
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_sv_file(consts.NETWORK_ACCESS_LOGS_SV_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        allow_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)

        rules_dict = remove_conflicting_rules(combine_allow_and_block_rules_dict(allow_rules_dict, block_rules_dict))
        
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.block and args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        block_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)
        allow_rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)

        rules_dict = remove_conflicting_rules(combine_allow_and_block_rules_dict(allow_rules_dict, block_rules_dict))

        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.block:
        consts.NETWORK_BLOCK_APP_NAMES_PATH = args.block
        consts.RULES_FILE_PATH = args.output

        mod.process_block_file(consts.NETWORK_BLOCK_APP_NAMES_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, False)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.input:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.input
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_file(consts.NETWORK_ACCESS_LOGS_SV_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)
    elif args.recursive:
        consts.NETWORK_ACCESS_LOGS_SV_PATH = args.recursive
        consts.RULES_FILE_PATH = args.output

        mod.process_sv_directory(consts.NETWORK_ACCESS_LOGS_SV_PATH, args.simplified, consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH)

        rules_dict = create_final_rules_dict(consts.NETWORK_ACCESS_LOGS_CSV_OUTPUT_PATH, True)
        save_rules_file(rules_dict, consts.RULES_FILE_PATH, args.format)

if __name__ == "__main__":
    main()
