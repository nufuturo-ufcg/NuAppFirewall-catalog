import json

def write_json(dictionary, output_file):
    """
    Writes dictionary data to a JSON file.

    Args:
    dictionary (list): Dictionary of rules.
    output_file (str): Path to the output JSON file. 

    Author: Marcelo Vitorino <marcelo.vitorino@copin.ufcg.edu.br>
    """
    with open(output_file, 'w') as file:
        json.dump(dictionary, file, indent=4)
