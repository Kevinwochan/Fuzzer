import xml.etree.ElementTree as ET


def xml_corpus_files(files):
    tags = set()
    attributes = dict()
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        extract_xml_corpus(root, tags, attributes)
    return (tags, attributes)


def xml_corpus(file):
    tags = set()
    attributes = dict()
    tree = ET.parse(file)
    root = tree.getroot()
    extract_xml_corpus(root, tags, attributes)
    return (tags, attributes)

def extract_xml_corpus(node, tags, attributes):
    tags.add(node.tag)
    attr = node.attrib
    for k,v in attr.items():
        if k not in attributes: attributes[k] = set()
        attributes[k].add(v)

    for child in node:
        extract_xml_corpus(child, tags, attributes)
    

