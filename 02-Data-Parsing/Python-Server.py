from flask import Flask, jsonify, request
import json
import yaml
import csv
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Base path
BASE_PATH = 'C:/Users/eqwoa/System-Integration-Mandatory-Assignments/01-Data-Parsing'


def parse_txt(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {child.tag: child.text for child in root}

file_parsers = {
    'txt': parse_txt,
    'json': parse_json,
    'yaml': parse_yaml,
    'csv': parse_csv,
    'xml': parse_xml
}


@app.route('/', methods=['GET'])
def parse_file_request():
    file_name = request.args.get('file')  
    if not file_name:
        return jsonify({'error': 'File name is required'}), 400

    file_ext = file_name.split('.')[-1]  
    file_path = os.path.join(BASE_PATH, file_name)

    if file_ext in file_parsers:
        try:
            data = file_parsers[file_ext](file_path)
            return jsonify(data), 200
        except FileNotFoundError:
            return jsonify({'error': 'File not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Unsupported file type'}), 400


if __name__ == '__main__':
    app.run(debug=True)
