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

1. **Download or Clone Repository**: If you haven't already, download or clone the repository containing the rules-catalog/ folder to your local machine.

    ```bash
    git clone https://github.com/nufuturo-ufcg/nu-app-firewall-catalog.git
    ```

2. **Navigate to Repository Directory**: Open a terminal or command prompt and navigate to the directory where you downloaded or cloned the repository. You can use the cd command followed by the path to the directory.

    ```bash
    cd path/to/repository/rules-catalog/
    ```

3. **Modify consts.py**: Open the consts.py file in a text editor of your choice. Replace the placeholder values. Save and close the consts.py file.

4. **Install Dependencies**: Ensure you have Python installed and run the following command to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. **Prepare Your Data**: Make sure you have the Cortex XDR logs that you want to use for creating the rules catalog.

6. **Run the Main Script**: Use the `main.py` script located in the `rules-catalog` directory to generate the rules catalog:

   ```bash
   python main.py
   ```

   This script will process the data and create a catalog in .json based on the predefined mappings.

7. **Output .plist file**: If needed to output .plist file instead of json, please run the following code :

   ```bash
   python main.py -o plist
   ```
8. **Run tests**: Run all tests in subdirectory /test file using --test by executing the following command:

   ```bash
   python main.py --test
   ```

This process will generate a rules catalog that can be used with Nu-App Firewall, ensuring your configurations are correctly applied. 

For more details, refer to the specific README files in each module's directory.