import json
import yaml
import csv
import xml.etree.ElementTree as ET


#too many parsers

#text-based parse
def parse_text(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

#json based parse
def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

#yaml based parse
def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

#csv based parse
def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

#xml based parse
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: {child.tag: child.text for child in root}}

# Read & parse files
print("Text File:", parse_text("about-me.txt"))
print("JSON File:", parse_json("about-me.json"))
print("YAML File:", parse_yaml("about-me.yaml"))
print("CSV File:", parse_csv("about-me.csv"))
print("XML File:", parse_xml("about-me.xml"))
