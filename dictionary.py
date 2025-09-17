import json
def load_json(file_path:str):
    """returns file contents of a JSON-file 

    Args:
        file_path (str): string of the file path
    Returns:
        dict : file contents
    """
    with open(file_path,"r")as json_file:
        file_content : dict = json.load(json_file)
    return file_content

LEXICON = load_json("dictionary.json")
interface_guide= load_json("interface_guide.json")
SUGGESTIONS = interface_guide["SUGGESTIONS"]