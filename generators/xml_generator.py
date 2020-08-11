import xml.etree.ElementTree as ET
#import generators.corpus as corpus
import corpus
import random

class XmlGenerator:
    """
    mutator = Mutator("some_strings")
    mutated_str = mutator.mutate()
    """

    def __init__(self, tags, attributes, input_str: str = ""):
        self.input_str = input_str
        self._is_empty = False
        self.tags = tags
        self.attributes = attributes
        self.list_tags = list(tags)
        self.list_attr = self.listify_attr(attributes) #will this cause a corrupted constuction
        self.attr_limit = 3
        self.max_children = 4
        self.max_ancestors = 4


    def listify_attr(self, attributes):
        list_attr = []

        for attr, datas in attributes.items():
            data_list = [x for x in datas]
            list_attr.append((attr, data_list))

        return list_attr


    def rand_tag(self):
        n_tags = len(self.tags)
        i = random.randrange(n_tags)
        return self.list_tags[i]

    def rand_attr_data(self):
        n_attr = len(self.list_attr)
        atrr_i = random.randrange(n_attr)
        attr = self.list_attr
        datas = attr[1]
        n_datas = len(datas)
        datas_i = random.randrange(n_datas)

        attr = attr[0]
        val = datas[datas_i]
        return (attr, val)


    """
    creates a generator that generates different xml files randomly using a corpus
    """

    def generate(self) -> str:

        for i in range(6):
            self.max_ancestors += i
            for j in range(6):
                self.max_children += j
                xml = self.generate_xml()
                yield ET.tostring(xml, encoding='utf8', method='xml').decode('utf8')
        
        for i in range(1,7):
            xml = self.deep_nest(10**i)
            yield self.deep_str(xml)


    #also try to build a dense one so malloc runs out

    def deep_nest(self, iterations):
        root = self.generate_node()
        self.apply_attr(root)
        curr = root
        for i in range(iterations):
            curr = self.generate_child(curr)
        return root

    def opening_str(self, node):
        open_str = '<' + node.tag
        for attr, val in node.items():
            open_str += ' ' + attr + '=' '"' + val +'"'
        open_str += '>' + node.text
        return open_str

    def closing_string(self, node):
        return '</' + node.tag + '>' + node.tail

    def deep_str(self, root):
        head = ''
        tail = ''
        curr = root
        flag = True
        while(flag):
            flag = False
            head += self.opening_str(curr)
            tail = self.closing_string(curr) + tail
            for child in curr:
                # print(curr)
                # print(child)
                flag = True
                curr = child
        return head + tail


    #maybe unecessary duplication prevention...because a dict, would not have duplicates so valid xml
    def apply_attr(self, node):
        n_attr = len(self.list_attr)
        indexes = [i for i in range(n_attr)]
        random.shuffle(indexes)

        limit = random.randrange(self.attr_limit)

        for i, v in enumerate(indexes):
            if i >= limit: break
            attr, datas = self.list_attr[v]
            n_datas = len(datas)
            data_i = random.randrange(n_datas)
            data = datas[data_i]
            node.attrib[attr] = data

    def generate_xml(self):
        root = self.generate_node()
        self.generate_children(root, 0)
        return root

    def generate_node(self):
        tag = self.rand_tag()
        #attr, val = self.rand_attr_data()
        root = ET.Element(tag)
        self.apply_attr(root)
        root.text = '\n'
        root.tail = '\n'
        return root

        # for i in random.randrange(self.attr_limit):
        #     attr, 

    def generate_child(self, parent):
        tag = self.rand_tag()
        child = ET.SubElement(parent, tag)
        self.apply_attr(child)
        child.text = '\n'
        child.tail = '\n'
        return child

    def generate_children(self, parent, n_ancestors):
        if n_ancestors >= self.max_ancestors: return

        max = random.randrange(self.max_children + 1)
        for children_i in range(max):
            tag = self.rand_tag()
            child = ET.SubElement(parent, tag)
            self.apply_attr(child)
            child.text = '\n'
            child.tail = '\n'
            self.generate_children(child, n_ancestors+1)


    def set_input_str(self, input_str: str) -> None:
        self.input_str = input_str
        self._is_empty = False

    @property
    def is_empty(self) -> bool:
        """
        If a mutator has run out of payloads
        """
        return self._is_empty

    @is_empty.setter
    def is_empty(self, boolean):
        self._is_empty = boolean



#should test largest unsigned integer value
#manipulate the original raw data instead of the dictionary so spaces are preserved....can I do my own printing thing

if __name__ == "__main__":
    files = []
    files.append('files/xml1.txt')
    files.append('files/xml2.txt')
    files.append('files/xml3.txt')

    tags, attributes = corpus.xml_corpus_files(files)
    
    xml_gen = XmlGenerator(tags, attributes)
    xml = xml_gen.deep_nest(100000)
    xml_str = xml_gen.deep_str(xml)
    print(xml_str)
    # xml_str = ET.tostring(xml, encoding='utf8', method='xml')
    # print(xml_str.decode('utf8'))
    # xml_str = xml_gen.generate()
    # print(xml_str.decode('utf8'))

