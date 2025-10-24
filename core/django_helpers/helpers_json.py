import json
import os

def read_json(path):
    """Read JSON file and return as dict"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def write_json(path, data, indent=4):
    """Write dict/list to JSON file"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    return path

def parse_json(json_str):
    """Parse JSON string into dict/list"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None

def to_json(data, indent=4):
    """Convert dict/list to JSON string"""
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except (TypeError, ValueError):
        return None
    
"""
Example usage

from django_helpers import helpers_json

data = {"name": "Alice", "age": 25}

# Write JSON file
helpers_json.write_json("data.json", data)

# Read JSON file
print(helpers_json.read_json("data.json"))

# Parse JSON string
json_str = '{"city": "Paris", "country": "France"}'
print(helpers_json.parse_json(json_str))

# Convert to JSON string
print(helpers_json.to_json(data))

"""