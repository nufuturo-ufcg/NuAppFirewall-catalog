# Nu App Firewall Catalog

This repository contains tools for managing and creating rule catalogs for the Nu App Firewall. It includes scripts and modules for data analysis, rule mapping, and handling different file formats such as JSON and plist.

## Repository Structure

```plaintext
.
├── catalog.json                  # Example rule catalog in JSON format
├── catalog.plist                 # Example rule catalog in plist format
├── README.md                     # Repository documentation
└── rules-catalog                 # Main directory with scripts and modules
    ├── config
    │   ├── consts.py             # Constants used in the project
    ├── main.py                   # Main script for catalog creation and management
    ├── managers
    │   └── rule_manager.py       # Manages rules and their operations
    ├── mappers
    │   └── rule_mapper.py        # Maps rules according to Cortex XDR logs
    ├── module
    │   ├── cortex_analysis.py    # Module for analyzing Cortex XDR logs
    │   └── README.md             # Module documentation
    ├── README.md                 # Catalog documentation
    ├── requirements.txt          # Project dependencies
    ├── test
    │   └── test_rule_mapper.py   # Tests for rule mapping
    └── utils
        ├── csv_helper.py         # Helper for handling CSV files
        ├── json_helper.py        # Helper for handling JSON files
        ├── plist_helper.py       # Helper for handling plist files
```

## How to Create a Rules Catalog

Follow these steps:

1. **Download or Clone Repository**: If you haven't already, download or clone the repository containing the `rules-catalog/` folder to your local machine.

    ```bash
    git clone https://github.com/nufuturo-ufcg/nu-app-firewall-catalog.git
    ```

2. **Navigate to Repository Directory**: Open a terminal or command prompt and navigate to the directory where you downloaded or cloned the repository.

    ```bash
    cd path/to/repository/rules-catalog/
    ```

3. **Install Dependencies**: Ensure you have Python installed and run the following command to install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. **Prepare Your Data**: Ensure you have the Cortex XDR logs that you want to use for creating the rules catalog.

5. **Run the main script**: The main.py script, located in the rules-catalog directory, is used to generate the rules catalog in JSON format. Depending on the input type, you can use one of the following flags:

    - `-i`: For a single input CSV/TSV file.
    - `-r`: For a directory containing multiple CSV/TSV files.
    - `-b`: For a CSV file containing app names and their respective identifiers to generate block rules.
    - `--port-blocking`: For a TXT file containing ports that should be blocked system-wide.

        
    **Examples**

    Generate a Catalog from a Single Input File.
    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog
    ```

    Generate a Catalog from a Directory.
    ```bash
    python main.py -r path/to/network_access_logs_directory/ -o path/to/output_catalog
    ```

    Generate Block Rules from a CSV File.
    ```bash
    python main.py -b path/to/block_apps.csv -o path/to/output_catalog
    ```

    Generate System-Wide Port Blocking Rules from a TXT File.
    ```bash
    python main.py --port-blocking path/to/block_ports.txt -o path/to/output_catalog
    ```

    **Note that the `-b` and/or `--port-blocking` flag can be used in combination with either `-i` or `-r` to apply block rules to the generated catalog.**

6. **Output in .plist Format**: To generate a `.plist` output instead of JSON the script provides two options:

    **--plist**: To generate a binary plist output:
    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --plist
    ```

    **--plist-xml**: To generate an XML plist output:
    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --plist-xml
    ```

7. **Rule Simplification**: To generate a simplified rules catalog, use the --simplified flag, which groups frequent destinations.

    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --simplified
    ```

8. **Run Tests**: To run all tests located in the `/test` directory, use the `--test` flag:

    ```bash
    python main.py --test
    ```

This process will generate a rules catalog compatible with the Nu-App Firewall, ensuring your configurations are applied correctly.

For more details, refer to the specific README files in each module's directory.