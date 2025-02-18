from flask import Flask, jsonify, request
import json
import yaml
import csv
import os
import xml.etree.ElementTree as ET

#dependencies, pyyaml, flask

app = Flask(__name__)

# Base path for data files
BASE_PATH = 'C:/Users/eqwoa/Desktop/System-Integration-Mandatory-Assignments/01-Data-Parsing'

# Parse TXT File
def parse_txt(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Parse JSON File
def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Parse YAML File
def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Parse CSV File
def parse_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Parse XML File
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    result = {}
    for child in root:
        result[child.tag] = child.text
    return result

# Endpoints

@app.route('/parse_txt', methods=['GET'])
def get_txt_data():
    file_name = request.args.get('file', 'about-me.txt')
    file_path = os.path.join(BASE_PATH, file_name)
    try:
        data = parse_txt(file_path)
        return jsonify({'data': data}), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/parse_json', methods=['GET'])
def get_json_data():
    file_name = request.args.get('file', 'about-me.json')
    file_path = os.path.join(BASE_PATH, file_name)
    try:
        data = parse_json(file_path)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/parse_yaml', methods=['GET'])
def get_yaml_data():
    file_name = request.args.get('file', 'about-me.yaml')
    file_path = os.path.join(BASE_PATH, file_name)
    try:
        data = parse_yaml(file_path)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/parse_csv', methods=['GET'])
def get_csv_data():
    file_name = request.args.get('file', 'about-me.csv')
    file_path = os.path.join(BASE_PATH, file_name)
    try:
        data = parse_csv(file_path)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/parse_xml', methods=['GET'])
def get_xml_data():
    file_name = request.args.get('file', 'about-me.xml')
    file_path = os.path.join(BASE_PATH, file_name)
    try:
        data = parse_xml(file_path)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
