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
    │   └── rule_mapper.py        # Maps rules according to EDR logs
    ├── module
    │   ├── log_analysis.py    # Module for analyzing EDR logs
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

4. **Prepare Your Data**: Ensure you have the EDR logs that you want to use for creating the rules catalog.

5. **Run the main script**: Use the `main.py` script located in the `rules-catalog` directory to generate the rules catalog by providing the input CSV file with `-i` and providing the path to the output with `-o`:

    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog
    ```

    This will process the input CSV file and generate a catalog in JSON format.

6. **Output in .plist Format**: To generate a `.plist` output instead of JSON, run the script with the following command:

    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --plist-format xml
    ```

7. **Run Tests**: To run all tests located in the `/test` directory, use the `--test` flag:

    ```bash
    python main.py --test
    ```

This process will generate a rules catalog compatible with the Nu-App Firewall, ensuring your configurations are applied correctly.

For more details, refer to the specific README files in each module's directory.