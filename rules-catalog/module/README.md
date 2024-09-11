# Cortex Analysis

`Cortex Analysis` is a Python module for analyzing IPs and hostnames data. It provides functions to find hostnames, merge DataFrames, extract domains and subdomains, filter applications in a DataFrame, and generate frequency tables in HTML format.

## Usage

Enter the Python interpreter and import this module with the following command:

```python
import cortex_analysis
```

### Available Functions

#### `find_hostnames(df)`

Finds hostnames for IPs that do not have a hostname in the provided DataFrame.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame containing the columns `dst_action_external_hostname` and `action_remote_ip`.

**Returns:**
- `pd.DataFrame`: DataFrame with IPs and their respective hostnames.

#### `merge_dataframes(df1, df2)`

Merges two DataFrames on the columns `action_remote_ip` and `IP`, and updates the `dst_action_external_hostname` column.

**Parameters:**
- `df1 (pd.DataFrame)`: First DataFrame.
- `df2 (pd.DataFrame)`: Second DataFrame with the columns `IP` and `Hostname`.

**Returns:**
- `pd.DataFrame`: Merged DataFrame with updated `dst_action_external_hostname`.

#### `extract_main_domain(hostname)`

Extracts the main domain from a hostname.

**Parameters:**
- `hostname (str)`: Hostname to extract the main domain.

**Returns:**
- `str`: Extracted main domain.

#### `extract_main_subdomain(hostname)`

Extracts the main subdomain from a hostname.

**Parameters:**
- `hostname (str)`: Hostname to extract the main subdomain.

**Returns:**
- `str`: Extracted main subdomain.

#### `extract_registered_domain(hostname)`

Extracts the registered domain from a hostname.

**Parameters:**
- `hostname (str)`: Hostname to extract the registered domain.

**Returns:**
- `str`: Extracted registered domain.

#### `get_domain(df)`

Adds new columns to the DataFrame to store the main domain, main subdomain, and registered domain.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame that must contain the `dst_action_external_hostname` column.

**Returns:**
- `pd.DataFrame`: Updated DataFrame with additional columns `main_domain`, `main_subdomain`, and `registered_domain`.

**Raises:**
- `ValueError`: If the `dst_action_external_hostname` column contains null values.

#### `generate_table_html_hostnames(freq, hostnames, caption, column)`

Generates an HTML table for the frequency of a column with hostnames.

**Parameters:**
- `freq (pd.DataFrame)`: DataFrame containing the frequency of the values.
- `hostnames (dict)`: Dictionary mapping values to hostnames.
- `caption (str)`: Caption for the HTML table.
- `column (str)`: Column name.

**Returns:**
- `str`: HTML table as a string.

#### `save_frequency_table_hostnames_to_html(df, column, file_path)`

Saves the frequency table of IPs to an HTML file.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame containing the IP column.
- `column (str)`: Column name.
- `file_path (str)`: Path to save the HTML file.

**Returns:**
- `None`

#### `generate_table_html(freq, caption, column)`

Generates an HTML table for the frequency of a column.

**Parameters:**
- `freq (pd.Series)`: Series containing the frequency of the values.
- `caption (str)`: Caption for the HTML table.
- `column (str)`: Column name.

**Returns:**
- `str`: HTML table as a string.

#### `save_frequency_table_to_html(df, column, file_path)`

Saves the frequency table of a DataFrame column to an HTML file.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame containing the column.
- `column (str)`: Column name.
- `file_path (str)`: Path to save the HTML file.

**Returns:**
- `None`

#### `is_application_in_path(path, app)`

Checks if the application string is present in the provided path string.

**Parameters:**
- `path (str)`: Path string to search.
- `app (str)`: Application string to search for.

**Returns:**
- `bool`: True if the application string is found in the path string, False otherwise.

#### `filter_app(df, app, columns=None)`

Filters a DataFrame to include only rows where a specified application string is found in the provided columns or in the `'causality_actor_process_image_path'` column.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame to be filtered.
- `app (str)`: Application string to search for.
- `columns (list[str], optional)`: List of column names to search. Default is None, meaning if no columns are specified, all present in the passed DataFrame will be used.

**Returns:**
- `pd.DataFrame`: A new DataFrame containing only rows where the application string is found in the specified columns or in the `'causality_actor_process_image_path'` column.

**Raises:**
- `ValueError`: If none of the specified columns are found in the DataFrame.

#### `save_csv(df, output_file)`

Saves a DataFrame to a CSV file.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame to be saved.
- `output_file (str)`: Path to the output CSV file.

**Returns:**
- `None`

#### `save_apps_csv(df, applications, directory)`

Saves a filtered version of the DataFrame to CSV files for each application.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame to be filtered and saved.
- `applications (list[str])`: List of application names to filter the DataFrame.
- `directory (str)`: Directory where the CSV files will be saved.

**Returns:**
- `None`

#### `is_standard_application(path, applications)`

Checks if any of the standard application names are present in the provided file path.

**Parameters:**
- `path (str)`: File path to be checked.
- `applications (list[str])`: List of standard application names to search for.

**Returns:**
- `bool`: True if any of the application names are found in the file path, False otherwise.

#### `filter_standard_applications(df, applications)`

Identifies and filters standard applications in a DataFrame based on process image paths.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame containing the following columns:
    - `os_actor_process_image_path` (str): File path of the OS actor process image.
    - `causality_actor_process_image_path` (str): File path of the causal actor process image.
- `applications (list[str])`: List of standard application names to search for.

**Returns:**
- `pd.DataFrame`: DataFrame filtered to include only rows where both `os_actor_process_image_path` and `causality_actor_process_image_path` match standard applications.

#### `find_app_to_domain(df, apps)`

Associates registered domains with standard applications based on process image paths.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame containing the following columns:
    - `registered_domain` (str): Registered domain.
    - `os_actor_process_image_path` (str): File path of the OS actor process image.
- `apps (list[str])`: List of standard application names to search for.

**Returns:**
- `pd.DataFrame`: DataFrame containing the registered domains and associated applications, where each row represents a domain and its associated applications.

#### `combination_host_and_path(df)`

Generates a DataFrame mapping hosts (registered domains) to all paths in the `causality_actor_process_image_path` column.

**Parameters:**
- `df (pd.DataFrame)`: DataFrame with the following columns:
    - `causality_actor_process_image_path` (str): Path corresponding to the process responsible for the event.
    - `registered_domain` (str): Registered main domain.

**Returns:**
- `pd.DataFrame`: DataFrame containing all unique combinations of paths and registered domains.

#### `process_csv(input_csv_path, output_csv_path)`

Processes a CSV file and generates a new CSV file with the association between paths and all possible endpoints, grouped by all recorded events.

**Parameters:**
- `input_csv_path (str)`: Path to the input CSV file.
- `output_csv_path (str)`: Path to save the resulting CSV file.

**Returns:**
- None: The function does not return a value; it writes directly to the specified output path.