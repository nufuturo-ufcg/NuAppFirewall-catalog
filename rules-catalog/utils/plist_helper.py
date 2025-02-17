import plistlib

def bin_to_plist(bin_file_path, plist_file_path):
    """
    Convert binary data from a .bin file to a Property List (.plist) file.

    Parameters:
        bin_file_path (str): Path to the input binary (.bin) file.
        plist_file_path (str): Path to the output Property List (.plist) file.

    Raises:
        FileNotFoundError: If the input binary file does not exist.
        IOError: If there is an error reading or writing files.

    Notes:
        This function assumes that the binary data in the .bin file can be
        directly converted to a Python dictionary. If the binary data is in a
        different format, additional processing may be required.
    
    Author: Marcelo Vitorino <marcelo.vitorino@copin.ufcg.edu.br>
    """
    with open(bin_file_path, 'rb') as bin_file:
        binary_data = bin_file.read()

    plist_data = plistlib.loads(binary_data)

    write_plist(plist_data, plist_file_path)


def write_plist(dictionary, output_file, plist_format):
    """
    Writes rule dictionary data to a plist file.

    Args:
    dictionary (list): Dictionary of rules.
    output_file (str): Path to the output JSON file. 

    Author: Marcelo Vitorino <marcelo.vitorino@copin.ufcg.edu.br>
    """
    try:
        with open(output_file, 'wb') as plist_file:
            plistlib.dump(dictionary, plist_file, fmt=plist_format)
        print(f"Data successfully written to {output_file}.")
    except Exception as e:
        print(f"Error writing data to {output_file}: {e}")
