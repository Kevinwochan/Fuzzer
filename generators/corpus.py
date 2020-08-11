import xml.etree.ElementTree as ET

XML_TEXT = '''<html>
    <head>
        <link href="http://somewebsite.com" />
    </head>
    <body>
        <h1>I'm not a web developer. still</h1>
    </body>

    <div id="#lol">
        <a href="http://google.com">Here is some link...</a>
    </div>


    <tail>
        <a href="http://bing.com">Footer link</a>
    </tail>
</html>'''


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
    tree = ET.fromstring(file)
    # root = tree.getroot()
    root = tree
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
    

