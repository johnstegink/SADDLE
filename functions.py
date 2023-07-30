import hashlib
import os
import shutil
import sys
from pathlib import Path
from lxml import etree as ET
import numpy as np


def hash_string(to_be_hashed):
    """
    Creates a hash string of the string, only for uniqueness
    """

    hash_object = hashlib.sha1(to_be_hashed.encode())
    return hash_object.hexdigest()


def create_directory_if_not_exists(dir_name):
    """
    Creates a directory if it doesn't exist
    :param dir_name:
    :return:
    """

    os.makedirs( dir_name, exist_ok=True)
    # delete all files
    for file in read_all_files_from_directory( dir_name, "*"):
        os.remove(file)


def create_directory_for_file_if_not_exists( filename):
    """
    Creates the directory for the file if not does not exist
    """

    os.makedirs( os.path.dirname( filename), exist_ok=True)


def remove_redirectory_recursivly( dir_name):
    shutil.rmtree( dir_name)


def read_all_files_from_directory(dir_name, extension):
    """
    Read all files from a directory, recursively
    :param dir_name:
    :param extension
    :return:
    """
    return list( Path(dir_name).rglob("*." + extension))


def read_file(filename):
    """
    Read entire text of file
    :param filename: path to the file
    :return: contents of file
    """

    file = open( filename, mode="r", encoding="utf-8-sig")
    contents = file.read()
    file.close()

    return contents


def write_file(filename, contents):
    """
    Write text contents to a file
    :param filename: path to the file
    :param contents: textcontents
    :return: -
    """

    file = open( filename, mode="w", encoding="utf-8-sig")
    file.write( contents)
    file.close()



def xml_as_string(element):
    """
    Create xml string of the element
    :param element:
    :return:
    """
    return ET.tostring(element, encoding='unicode', method='xml', pretty_print=True)

def create_chunks_of_list(theList, chunk_size):
    """
    Splits a list into lists with chunks
    :param theList:
    "param chunk_size
    :return:
    """

    return [theList[i:i + chunk_size] for i in range(0, len(theList), chunk_size)]


def translate_language_code(language_code):
    """
    Translate the language code to a language for nltk-data
    :param language_code:
    :return:
    """
    code = language_code.lower()
    if code == 'en' or code == 'simple':
        return "english"
    elif code == 'nl':
        return 'dutch'
    else:
        raise Exception (f"Unknown language '{language_code}'")

def translate_language_into_code(language):
    """
    Translate the language for nltk-data into a language code
    :param language:
    :return:
    """
    lang = language.lower()
    if lang == 'english':
        return "en"
    elif lang == 'dutch':
        return 'nl'
    else:
        raise Exception (f"Unknown language '{lang}'")

def show_message( message):
    sys.stderr.write( message + "...\n")

def normalize_vector( vector):
    """
    Creates a unit vector of the given vector
    :param vector: list of floats
    :return: list of floats
    """
    v = np.array( vector)
    norm = np.linalg.norm( v)
    if norm == 0:
        return vector
    else:
        return (v / norm).tolist()

def write_corpus_info(corpusdir, name, language_code):
    """
    Write the corpus info
    :param corpusdir:
    :param name:
    :param language_code:
    :return:
    """
    root = ET.fromstring("<corpus></corpus>")
    ET.SubElement( root, "name").text = name
    ET.SubElement( root, "language_code").text = language_code

    write_file( os.path.join( corpusdir, "corpus.info"), xml_as_string( root))


def read_corpus_info(corpusdir):
    """
    Reads the corpus info
    :param corpusdir:
    :return: (name, language_code)
    """

    doc = ET.parse(os.path.join( corpusdir, "corpus.info"))
    corpus = doc.getroot()
    name = corpus.find("name").text
    language_code = corpus.find("language_code").text

    return (name, language_code)

def write_article_pairs( corpusdir, info):
    """
    Write a .tsv with articlepairs to the corpus, the file is name pairs.tsv
    :param corpusdir: Directory containing the corpus
    :param info: list of tuples (id1, id2, similarity) where similarity is 0 or 1
    :return:
    """

    file = open(os.path.join(corpusdir, "pairs.tsv"), mode="w", encoding="utf-8-sig")
    for record in info:
        file.write(f"{record[0]}\t{record[1]}\t{record[2]}\n")
    file.close()

def read_article_pairs( corpusdir):
    """
    Read a .tsv with articlepairs to the corpus, created by write_article_pairs
    :param corpusdir: Directory containing the corpus
    :return: list of tuples (id1, id2, similarity) where similarity is 0 or 1
    """

    file = open(os.path.join(corpusdir, "pairs.tsv"), mode="r", encoding="utf-8-sig")
    lines = file.readlines();
    file.close()

    info = []
    for line in lines:
        record = line.split("\t")
        info.append( (record[0], record[1], float(record[2])))

    return info

def copy_dir( src_dir, dest_dir):
    """
    Makes a copy from the files in the srcdir to to destdir
    :param src_dir:
    :param dest_dir:
    :return:
    """

    create_directory_if_not_exists( dest_dir)
    for file_name in os.listdir(src_dir):
        source = os.path.join(src_dir, file_name)
        destination = os.path.join(dest_dir, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)

