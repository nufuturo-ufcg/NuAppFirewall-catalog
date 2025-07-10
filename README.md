# Nu App Firewall Catalog

This repository contains tools for managing and creating rule catalogs for the NuAppFirewall, [available at this repository](https://github.com/nufuturo-ufcg/NuAppFirewall). It includes scripts and modules for data analysis, rule mapping, and handling different file formats such as JSON and plist.

## Repository Structure

```plaintext
.
├── Dockerfile                    # Dockerfile file
├── LICENSE
├── README.md                     # Repository documentation
├── data                          # Data repository
├── docker-compose.yml            # docker-compose file
└── rules-catalog                 # Main directory with scripts and modules
    ├── README.md                 # Catalog documentation
    ├── config
    │   └── consts.py             # Constants used in the project
    ├── data
    ├── main.py                   # Main script for catalog creation and management
    ├── managers
    │   └── rule_manager.py       # Manages rules and their operations
    ├── mappers
    │   └── rule_mapper.py        # Maps rules according to EDR logs
    ├── module
    │   ├── README.md             # Module documentation
    │   └── log_analysis.py       # Module for analyzing EDR logs
    ├── requirements.txt          # Project dependencies
    └── utils
        ├── csv_helper.py         # Helper for handling CSV files
        ├── json_helper.py        # Helper for handling JSON files
        ├── main_helper.py        # Helper for handling main function
        └── plist_helper.py       # Helper for handling PLIST files
```

## How to Create a Rules Catalog

1. **Download or clone repository**: If you haven't already, download or clone the repository containing the `rules-catalog/` folder to your local machine.

    ```bash
    git clone https://github.com/nufuturo-ufcg/nu-app-firewall-catalog.git
    ```

2. **Navigate to repository directory**: Open a terminal or command prompt and navigate to the directory where you downloaded or cloned the repository.

    ```bash
    cd path/to/repository/rules-catalog/
    ```

You can use either a Python virtual environment or Docker to run the catalog generation tool:

### Option A: Using Python Virtual Environment (`venv`)

1. **Create and activate a virtual environment**: Ensure you have Python installed and run the following command to create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies**: 

    ```bash
    pip install -r requirements.txt
    ```

4. **Prepare your data**: Ensure you have the EDR logs that you want to use for creating the rules catalog.

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

6. **Output in .plist format**: To generate a `.plist` output instead of JSON the script provides two options:

    **--plist**: To generate a binary plist output:
    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --plist
    ```

    **--plist-xml**: To generate an XML plist output:
    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --plist-xml
    ```

7. **Rule simplification**: To generate a simplified rules catalog, use the --simplified flag, which groups frequent destinations.

    ```bash
    python main.py -i path/to/network_access_logs.csv -o path/to/output_catalog --simplified
    ```

### Option B: Using Docker

1. **Builg the docker image**: From the root of the repository (where the `Dockerfile` and `docker-compose.yml` are located), build the container image.

    ```bash
    docker-compose build
    ```

2. **Prepare your data**: Place any input files (e.g. EDR logs, block rules, port lists) inside the data/ directory at the project root. This folder will be mounted into the container at runtime.

3. **Run the main script**: Use `docker-compose run` to execute the `main.py` script with the desired flags. Depending on the input type, you can use one of the following flags:

    - `-i`: For a single input CSV/TSV file.
    - `-r`: For a directory containing multiple CSV/TSV files.
    - `-b`: For a CSV file containing app names and their respective identifiers to generate block rules.
    - `--port-blocking`: For a TXT file containing ports that should be blocked system-wide.

    **Examples**

    Generate a Catalog from a Single Input File.
    ```bash
    docker-compose run --rm rules-catalog -i /path/to/network_access_logs.csv -o /path/to/output_catalog
    ```

    Generate a Catalog from a Directory.
    ```bash
    docker-compose run --rm rules-catalog -r /path/to/network_access_logs_directory/ -o /path/to/output_catalog
    ```

    Generate Block Rules from a CSV File.
    ```bash
    docker-compose run --rm rules-catalog -b /path/to/block_apps.csv -o /path/to/output_catalog
    ```

4. **Optional flags**: 

    - `--plist`: Output in binary `.plist` format.
    - `--plist-xml`: Output in XML `.plist` format.
    - `--simplified`: Simplified the generated catalog by grouping destinations.

This process will generate a rules catalog compatible with the Nu-App Firewall, ensuring your configurations are applied correctly.

For more details, refer to the specific README files in each module's directory.
