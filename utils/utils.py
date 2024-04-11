import json
import os


def load_file(path, file_name):
    file_path = os.path.join(os.path.dirname(__file__), path, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def filter_entities_and_exclude_key(json_input, exclude, key):
    return [entry for entry in json_input if all(word not in entry[key] for word in exclude)]


def filter_device(data, device, device_name):
    filtered_data = [item for item in data if
                     device.lower() in item['entity_id'].lower() and device_name.lower() in item['name'].lower()]
    return filtered_data


def fetch_function(name):
    return load_file('../functions', name)
