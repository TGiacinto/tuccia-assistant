import json
import os


def load_file(path, file_name):
    file_path = os.path.join(os.path.dirname(__file__),  path, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_function(name):
    return load_file('functions', name)
