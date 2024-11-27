import os
import re
import sys
import pandas as pd
import tldextract as tld
import ipaddress
import socket
import numpy as np

def find_hostnames(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find hostnames for IPs without a hostname in the given DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing the column 'dst_action_external_hostname' and 'action_remote_ip'.

    Returns:
        pd.DataFrame: DataFrame with IPs and their corresponding hostnames.
    """
    ips_without_hostname = df[df['dst_action_external_hostname'].isna()]['action_remote_ip'].unique()
    sorted_ips = sorted(ips_without_hostname, key=lambda ip: ipaddress.ip_address(ip))

    results = []
    for ip in sorted_ips:
        try:
            hostname = socket.gethostbyaddr(ip)
            results.append({'IP': ip, 'Hostname': hostname[0]})
        except socket.herror:
            results.append({'IP': ip, 'Hostname': "No DNS Record found"})

    return pd.DataFrame(results)


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Merge two DataFrames on 'action_remote_ip' and 'IP' columns and update 'dst_action_external_hostname'.

    Args:
        df1 (pd.DataFrame): First DataFrame.
        df2 (pd.DataFrame): Second DataFrame with 'IP' and 'Hostname' columns.

    Returns:
        pd.DataFrame: Merged DataFrame with updated 'dst_action_external_hostname'.
    """
    merged_df = df1.merge(df2, left_on='action_remote_ip', right_on='IP', how='left', right_index=False, left_index=False)

    merged_df['dst_action_external_hostname'] = merged_df.apply(
        lambda row: row['Hostname'] if pd.isna(row['dst_action_external_hostname']) else row['dst_action_external_hostname'],
        axis=1
    )

    merged_df.drop(['Hostname', 'IP'], axis=1, inplace=True)

    return merged_df


def is_ip(address: str):
    """
    Given an Address, verifies if it is an IP or not.

    Args:
        - address (str): The address to be verified.

    Returns:
        - bool: True if the address is an IP (IPv4 or IPv6) or else False.
    """

    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def get_domain_ip(ip: str) -> str:
    """
    Extract the URL of a given IP.

    Args:
        - ip (str): IP that will have an URL extracted from.
        
    Returns:
        - str: Extracted URL.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.gaierror, socket.herror):
        return "URL could not be retrieved"


def extract_main_domain(hostname: str) -> str:
    """
    Extract the main domain from a given hostname.

    Args:
        hostname (str): Hostname to extract the main domain from.

    Returns:
        str: Extracted main domain.
    """
    extracted = tld.extract(hostname)
    if extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    else:
        return hostname


def extract_main_subdomain(hostname: str) -> str:
    """
    Extract the main subdomain from a given hostname.

    Args:
        hostname (str): Hostname to extract the main subdomain from.

    Returns:
        str: Extracted main subdomain.
    """
    extracted = tld.extract(hostname)
    if extracted.suffix:
        return f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}"
    else:
        return hostname


def extract_registered_domain(hostname: str) -> str:
    """
    Extract the registered domain from a given hostname.

    Args:
        hostname (str): Hostname to extract the registered domain from.

    Returns:
        str: Extracted registered domain.
    """
    extracted = tld.extract(hostname)
    if extracted.registered_domain:
        return extracted.registered_domain
    else:
        return hostname
  

def get_domain(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds columns for main domain, main subdomain and registered domain to the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing column 'dst_action_external_hostname'.

    Returns:
        pd.DataFrame: DataFrame with additional columns 'main_domain', 'main_subdomain' and 'registered_domain'.
    """

    if df['dst_action_external_hostname'].isna().sum() > 0:
        raise ValueError("A coluna de hostnames não deve conter valores nulos.")
    
    df['main_domain'] = df['dst_action_external_hostname'].apply(extract_main_domain)
    df['main_subdomain'] = df['dst_action_external_hostname'].apply(extract_main_subdomain)
    df['registered_domain'] = df['dst_action_external_hostname'].apply(extract_registered_domain)
    
    return df


def generate_table_html_hostnames(freq: pd.DataFrame, hostnames: dict, caption: str, column: str) -> str:
    """
    Generate HTML table for collumn frequency with hostnames.

    Args:
        freq (pd.DataFrame): DataFrame containing frequency of IPs.
        hostnames (dict): Dictionary mapping IPs to hostnames.
        caption (str): Caption for the HTML table.
        column (str): Column name.

    Returns:
        str: HTML table as a string.
    """  
    table_html = f"""
    <table border="1" cellspacing="0" cellpadding="5">
        <caption>{caption}</caption>
        <tr>
        <th>{column}</th>
        <th>Hostnames</th>
        <th>Counting Host</th>
        <th>Occurrences Log</th>
        </tr>
    """
    for index, row in freq.iterrows():
        content = row[column]
        hostname = ', '.join(hostnames.get(content, set()))
        counting_host = len(hostname.split(', '))
        occurences = row['count']
        table_html += f"<tr><td>{content}</td><td>{hostname}</td><td>{counting_host}</td><td>{occurences}</td></tr>"
    table_html += "</table>"
    
    return table_html


def generate_table_html(freq: pd.Series, caption: str, column: str) -> str:
    """
    Generate HTML table for frequency of a given column.

    Args:
        freq (pd.Series): Series containing frequency of values.
        caption (str): Caption for the HTML table.
        column (str): Name of the column.

    Returns:
        str: HTML table as a string.
    """
    table_html = f"""
    <table border="1" cellspacing="0" cellpadding="5">
        <caption>{caption}</caption>
        <tr>
        <th>{column}</th>
        <th>Frequency</th>
        </tr>
    """
    for index, value in freq.items():
        table_html += f"<tr><td>{index}</td><td>{value}</td></tr>"
    table_html += "</table>"

    return table_html


def save_frequency_table_hostnames_to_html(df: pd.DataFrame, column: str, file_path: str) -> str:
    """
    Save the ip frequency table in the DataFrame in an HTML file.
    
    Args:
        df (pd.DataFrame): DataFrame containing the IP column.
        column (str): Column name.
        file_path (str): Path to save the HTML file.

    Returns:
        None
    """
    hostnames = df.groupby(column)['dst_action_external_hostname'].apply(lambda x: set(x.dropna().astype(str))).to_dict()

    freq = df[column].value_counts().reset_index()
    freq.columns = [column, 'count']

    filtered_column = df[column].value_counts()
    print(f"Total of {column}: {filtered_column.count()}")
    
    table_html_ip = generate_table_html_hostnames(freq, hostnames, f"Frequency Table - {column}", column)
    with open(file_path, 'w') as file:
        file.write(table_html_ip)


def save_frequency_table_to_html(df: pd.DataFrame, column: str, file_path: str):
    """
    Save the frequency table of a given column in the DataFrame to an HTML file.

    Args:
        df (pd.DataFrame): DataFrame containing the column.
        column (str): Name of the column.
        file_path (str): Path to save the HTML file.

    Returns:
        None
    """
    filtered_column = df[column].value_counts()
    print(f"Total of {column}: {filtered_column.count()}")
    
    table_html = generate_table_html(filtered_column, f"Frequency Table - {column}", column)
    
    with open(file_path, 'w') as file:
        file.write(table_html)


def is_application_in_path(path: str, app: str) -> bool:
    """
    Check if the application string is present in the given path string.

    Args:
        path (str): The path string to search within.
        app (str): The application string to search for.

    Returns:
        bool: True if the application string is found in the path string, False otherwise.
    """
    return app.lower() in path.lower()


def filter_app(df: pd.DataFrame, app: str, columns: list[str] = None) -> pd.DataFrame:
    """
    Filter a DataFrame to include only rows where a specified application string is found in the given columns or in the 'causality_actor_process_image_path' column.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        app (str): The application string to search for.
        columns (list[str], optional): List of column names to search within. Defaults to None, which means all columns are searched.

    Returns:
        pd.DataFrame: A new DataFrame containing only the rows where the application string is found in the specified columns or in the 'causality_actor_process_image_path' column.

    Raises:
        ValueError: If none of the specified columns are found in the DataFrame.
    """
    if columns is None:
        columns = df.columns.tolist()

    valid_columns = [col for col in columns if col in df.columns]
    if not valid_columns:
        raise ValueError("No valid search columns found in DataFrame.")

    if 'causality_actor_process_image_path' in df.columns:
        app_filtered_df = df[df['causality_actor_process_image_path'].apply(lambda x: is_application_in_path(x, app))]

    return app_filtered_df[columns]


def save_csv (df: pd.DataFrame, output_file: str):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to be saved.
    - output_file (str): The path to the output CSV file.

    Returns:
    - None
    """
    df.to_csv(output_file, index=False)


def save_apps_csv(df: pd.DataFrame, applications: list[str], directory: str):
    """
    Saves a filtered version of the DataFrame to CSV files for each application.

    This function iterates over a list of applications, filters the DataFrame for each application,
    and saves the filtered DataFrame to a CSV file named after the application in the specified directory.

    Parameters:
    - df (pd.DataFrame): The DataFrame to be filtered and saved.
    - applications (list[str]): A list of application names to filter the DataFrame.
    - directory (str): The directory where the CSV files will be saved.

    Returns:
    - None
    """
    for app in applications:
        filtered_df = filter_app(df, app)
        output_file = directory + f'{app}.csv'
        if len(filtered_df) > 1:
            save_csv(filtered_df, output_file)

    
def is_standard_application(path: str, applications: list[str]) -> bool:
    """
    Checks if any of the standard application names are present in the given file path.

    Parameters:
    - path (str): The file path to check.
    - applications (list[str]): A list of standard application names to look for.

    Returns:
    - bool: True if any of the application names are found in the file path, False otherwise.
    """
    return any(app.lower() in path.lower() for app in applications)


def filter_standard_applications(df: pd.DataFrame, applications: list[str]) -> pd.DataFrame:
    """
    Identifies and filters standard applications in a DataFrame based on process image paths.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the following columns:
        - `os_actor_process_image_path` (str): File path for the OS actor process image.
        - `causality_actor_process_image_path` (str): File path for the causality actor process image.
    - applications (list[str]): A list of standard application names to look for.

    Returns:
    - pd.DataFrame: A DataFrame filtered to only include rows where both 
      `os_actor_process_image_path` and `causality_actor_process_image_path` correspond to standard applications.
    """
    df['is_standard_application'] = df.apply(
        lambda row: (
            is_standard_application(row['os_actor_process_image_path'], applications) and
            is_standard_application(row['causality_actor_process_image_path'], applications)
        ),
        axis=1
    )

    return df[df['is_standard_application']]


def find_app_to_domain(df: pd.DataFrame, apps: list[str]) -> pd.DataFrame:
    """
    Associates registered domains with standard applications based on process image paths.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the following columns:
        - `registered_domain` (str): The registered domain.
        - `os_actor_process_image_path` (str): File path for the OS actor process image.
    - apps (list[str]): A list of standard application names to look for.

    Returns:
    - pd.DataFrame: A DataFrame containing the registered domains and associated applications,
      where each row represents a domain and its associated applications.
    """
    results = []

    for domain in df['registered_domain'].unique():
        domain_df = df[df['registered_domain'] == domain]
        
        associated_apps = []
        for app in apps:
            if domain_df['os_actor_process_image_path'].apply(lambda x: is_application_in_path(x, app)).any():
                associated_apps.append(app)
        
        results.append({
            'registered_domain': domain,
            'dst_action_external_hostname': ', '.join(associated_apps)
        })

    return pd.DataFrame(results)


def combination_host_and_path(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters and removes duplicate combinations of process image paths and registered domains.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the following columns:
        - `causality_actor_process_image_path` (str): The path of the causality actor process image.
        - `registered_domain` (str): The registered domain.
    
    Returns:
    - pd.DataFrame: A DataFrame containing unique combinations of process image paths and registered domains,
      excluding records where `registered_domain` is 'No DNS Record found'.
    """

    df = df[df['registered_domain'] != 'No DNS Record found']
    
    unique_df = df.drop_duplicates(subset=['causality_actor_process_image_path', 'registered_domain'])
    
    return unique_df


def get_domains(endpoints: list[str], ip_urls_dict: dict) -> list[str]:
    """
    Given a list of endpoints, converts them to unique domains and returns a list of these domains.

    Args:
    - endpoints (list[str]): A list of endpoints.
    - ip_urls_dict (dict): A dictionary that maps an IP to its respective URL.

    Returns:
    - list[str]: A list of unique domains extracted from the endpoins given.
    """
    domains_set = set()
    
    for entry in endpoints:
        if is_ip(entry):
            if entry in ip_urls_dict:
                respective_url = ip_urls_dict[entry]
            else:
                respective_url = get_domain_ip(entry)
                ip_urls_dict[entry] = respective_url
            
            if respective_url != "URL could not be retrieved" and respective_url != "_gateway":
                domains_set.add(extract_main_domain(respective_url))
        else:
            domains_set.add(extract_main_domain(entry))

    return list(domains_set)


def read_sv_file(input_sv_file_path: str) -> pd.DataFrame:
    """
    Process a CSV or TSV file to generate a corresponding Pandas DataFrame.

    Parameters:
    - input_sv_file_path (str): The file path to the input CSV or TSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing all of the information given by the C/TSV file
      or None if the given file isn't a CSV or TSV.  
    """
    if re.match(r'^.*\.csv$', input_sv_file_path) is not None:
        return pd.read_csv(input_sv_file_path)
    elif re.match(r'^.*\.tsv$', input_sv_file_path) is not None:
        return pd.read_csv(input_sv_file_path, sep='\t')
    else:
        return None   


def filtered_df_to_intermediate_csv(filtered_df: pd.DataFrame, output_csv_path: str) -> None:
    """
    Convert a dataframe produced from EDR logs to an intermediate CSV on rules-catalog/data/

    This intermediate csv and its file path will be both be created at runtime if it wasn't
    created in a previous execution, and then a processed dataframe will be converted to this
    CSV.

    Args:
    - filtered_df (pd.Dataframe): Dataframe created from EDR logs with only the following columns:
      'causality_actor_process_image_path', 'action_remote_ip', 'action_remote_port' and 'dst_action_external_hostname'.
    - output_csv_path (str): The file path where the output CSV file will be saved.

    Returns:
    - None: The function writes the results directly to the specified output CSV file.
    
    Output CSV Structure:
    - causality_actor_process_image_path (str): The unique process image paths found in the original CSV.
    - destinations (set): A set of lists consisting of unique values from the 'action_remote_ip' and 
      'dst_action_external_hostname' columns with their associated 'action_remote_port' value.
    """
    def get_destinations(group):
        destinations = set()
        for _, row in group.iterrows():
            port = row['action_remote_port']
            if pd.isna(port):
                port = "any"
            else:
                port = int(port)

            if pd.notna(row['action_remote_ip']):
                destinations.add((row['action_remote_ip'], str(port)))
            if pd.notna(row['dst_action_external_hostname']):
                destinations.add((row['dst_action_external_hostname'], str(port)))

        return list(destinations)
    
    result = filtered_df.groupby('causality_actor_process_image_path').apply(get_destinations).reset_index()

    result.columns = ['causality_actor_process_image_path', 'destinations']

    result.to_csv(output_csv_path, index=False)


def process_block_file(input_block_file_path: str, output_csv_path: str) -> None:
    """
    Processes a TXT file that has an app to be blocked per line to generate a new CSV with unique
    subpaths and associated destinations.

    This function reads an input TXT file and for each line creates a line on a dataframe with the 
    respective columns: 'causality_actor_process_image_path', 'action_remote_ip', 'action_remote_port' 
    and 'dst_action_external_hostname', after that it sends this dataframe to an auxiliary function to
    write this dataframe to a new CSV file.

    Parameters:
    - input_bloc_file_path (str): The file path to the input TXT file.
    - output_csv_path (str): The file path where the output CSV file will be saved.
    
    Returns:
    - None: The function writes the results directly to the specified output CSV file.
    
    Output CSV Structure:
    - causality_actor_process_image_path (str): The unique process image paths based on each line of
      the TXT file with the following structure, "/Applications/{app_name}".
    - destinations (set): A set of lists consisting of unique values from the 'action_remote_ip' and 
      'dst_action_external_hostname' columns with their associated 'action_remote_port' value.
    """

    absolute_path = os.path.expanduser(input_block_file_path)

    with open(absolute_path, "r") as file:
        app_names = [line.strip() for line in file]

    data = {
        'causality_actor_process_image_path': [app for app in app_names],
        'action_remote_ip': [np.nan] * len(app_names),
        'action_remote_port': [np.nan] * len(app_names),
        'dst_action_external_hostname': ['any'] * len(app_names)
    }

    df = pd.DataFrame(data)

    filtered_df_to_intermediate_csv(df, output_csv_path)


def process_sv_file(input_sv_file_path: str, output_csv_path: str) -> None:
    """
    Processes a CSV or TSV file to generate a new CSV with unique paths and associated destinations.

    This function reads an input CSV or TSV file, filters and groups data by the unique paths found 
    in the 'causality_actor_process_image_path' column, and creates a set of associated 
    destinations from the 'action_remote_ip', 'dst_action_external_hostname' and 'action_remote_port' columns, 
    'action_remote_ip' and 'dst_action_external_hostname' with null or blank values are excluded. 
    The result is saved to a new CSV file.

    Parameters:
    - input_sv_file_path (str): The file path to the input CSV or TSV file.
    - output_csv_path (str): The file path where the output CSV file will be saved.
    
    Returns:
    - None: The function writes the results directly to the specified output CSV file.
    
    Output CSV Structure:
    - causality_actor_process_image_path (str): The unique process image paths found in the original CSV.
    - destinations (set): A set of lists consisting of unique values from the 'action_remote_ip' and 
      'dst_action_external_hostname' columns with their associated 'action_remote_port' value.
    """
    
    df = read_sv_file(input_sv_file_path)
    
    if df is None:
        print('The given file format is not supported, only CSV or TSV')
        sys.exit()

    df_filtered = df[['causality_actor_process_image_path', 'action_remote_ip', 'action_remote_port', 'dst_action_external_hostname']]
    df_filtered = df_filtered.dropna(subset=['action_remote_ip', 'dst_action_external_hostname'], how='all')

    filtered_df_to_intermediate_csv(df_filtered, output_csv_path)


def process_sv_directory(input_sv_directory_path: str, output_csv_path: str) -> None:
    """
    Processes a directory of CSV or TSV files to generate a new CSV with unique paths and associated destinations.

    This function reads an input directory, filters and groups data of its logs by the unique 
    paths found in the 'causality_actor_process_image_path' column, and creates a set of associated 
    destinations from the 'action_remote_ip', 'dst_action_external_hostname' and 'action_remote_port' columns, 
    'action_remote_ip' and 'dst_action_external_hostname' with null or blank values are excluded. 
    The result is saved to a new CSV file.

    Parameters:
    - input_sv_directory_path (str): The file path to the input directory of logs.
    - output_csv_path (str): The file path where the output CSV file will be saved.
    
    Returns:
    - None: The function writes the results directly to the specified output CSV file.
    
    Output CSV Structure:
    - causality_actor_process_image_path (str): The unique process image paths found in the original CSV.
    - destinations (set): A set of lists consisting of unique values from the 'action_remote_ip' and 
      'dst_action_external_hostname' columns with their associated 'action_remote_port' value.
    """
    absolute_path = os.path.expanduser(input_sv_directory_path)

    if not os.path.isdir(absolute_path):
        print("The given directory doesn't exist")
        sys.exit()

    df = None

    directory = os.scandir(absolute_path)
    for entry in directory :
        if entry.is_file() and df is None:
            df = read_sv_file(absolute_path + entry.name)
        elif entry.is_file() and df is not None:
            df_to_concat = read_sv_file(absolute_path + entry.name)
            
            if df_to_concat is not None:
                df = pd.concat([df, df_to_concat])

    if df is None:
        print("There is no CSV or TSV file inside the given directory")
        sys.exit()

    df_filtered = df[['causality_actor_process_image_path', 'action_remote_ip', 'action_remote_port', 'dst_action_external_hostname']]
    df_filtered = df_filtered.dropna(subset=['action_remote_ip', 'dst_action_external_hostname'], how='all')

    filtered_df_to_intermediate_csv(df_filtered, output_csv_path)