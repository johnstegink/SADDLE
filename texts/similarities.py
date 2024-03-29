# Class to read and write document similarities
import random

from texts.similarity import Similarity
from lxml import etree as ET
import functions

class Similarities:
    def __init__(self):
        self.similarities = {}

    def add(self, src, dest, similarity):
        """
        Add a document relation
        :param src: source id
        :param dest: destination id
        :param similarity: (0, 1 or 2)
        :param overwrite the value if it already added
        :return:
        """

        if not src in self.similarities:
            self.similarities[src] = {}

        self.similarities[src][dest] = Similarity(src, dest, similarity)


    def save(self, file, shuffled=False):
        """
        Save the similarities in the given Xml file
        :param file:the output file
        :param shuffled: true if the list is shuffled first
        :return:
        """

        # Collect all src and destination combinations first
        pairs = []
        for src in self.similarities.keys():
            for dest in self.similarities[src].keys():
                similarity = self.similarities[src][dest]
                pairs.append( (src, dest, similarity.get_similarity()))

        if shuffled:
            random.shuffle( pairs)

        root = ET.fromstring("<similarities></similarities>")
        for (src, dest, similarity) in pairs:
            document = ET.SubElement(root, "relation")
            ET.SubElement(document, "src").text = src
            ET.SubElement(document, "dest").text = dest
            ET.SubElement(document, "similarity").text = str(similarity)

        # Write the file
        functions.write_file( file, functions.xml_as_string(root))



    @staticmethod
    def read(file):
        """
        Returns a new Similarities object filled with the info in the Xml file
        :param file: xml file, that was created with a save
        :return: Similarities object
        """
        sim = Similarities()
        root = ET.parse(file).getroot()
        for document in root:
            src = document.find("src").text
            dest = document.find("dest").text
            similarity = int(document.find("similarity").text)
            sim.add( src, dest, similarity)

        return sim

    def get_similiarties(self, src):
        """
        Returns a list of similarities of the source
        :param src:
        :return: List of similarities
        """

        if src in self.similarities:
            return list( self.similarities[src].values())
        else:
            return []   # No similarities

    def get_all_similarities(self):
        """
        Returns a list with all similarities
        :return:
        """

        lst = []
        for src in self.similarities:
            for sims in self.similarities[src].values():
                lst.append(sims)

        return lst



    def __iter__(self):
        """
        Initialize the iterator
        :return:
        """
        self.id_index = 0
        self.keys = list(self.similarities.keys())
        return self

    def __next__(self):
        """
        Next similarity
        :return:
        """
        if self.id_index < len(self.keys):
            similarity = self.similarities[self.keys[self.id_index]]
            self.id_index += 1  # Ready for the next similarity
            return similarity

        else:  # Done
            raise StopIteration

    def count(self):
        """
        Count the number of similarities
        :return:
        """
        return len(self.similarities.keys())