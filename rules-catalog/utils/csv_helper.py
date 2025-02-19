import csv
import sys

maxInt = sys.maxsize
csv.field_size_limit(sys.maxsize)

def write_to_csv(logs_dict, output_file_path):
    """
    Saves the log dictionary to a CSV file.

    Args:
    data (list): A list of dictionaries containing the log data.
    """
    fieldnames = ['causality_actor_process_image_path', 'destinations']
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in logs_dict:
            writer.writerow(row)

    
def read_csv(logs_csv):
    """
    Reads data from a CSV file and returns a list of dictionaries.

    Args:
    logs_csv (str): Path to the CSV file.

    Returns:
    list: List of dictionaries representing the CSV data.
    """
    data = []
    with open(logs_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data
