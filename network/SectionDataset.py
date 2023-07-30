# Class implements a dataloader for corpus files. It uses a cache for the distance matrix
import pickle

import numpy

from texts.corpus import Corpus
from Distances.DocumentVectors import  DocumentVectors
from scipy.spatial import distance
import os
from statistics import mean

class SectionDataset:

    def __init__(self, N, corpus_dir, documentvectors_dir, transformation, cache_file):
        """
        Set variables and read or create the graph
        :param N the maximum number of sections i.e. the size of the vector will be NxN
        :param corpus_dir: the directory with the corpus containing the document pairs
        :param documentvectors_dir: the directory containing the documentvectors
        :param transformation: can either be 'truncate' or 'avg'
                               - truncate: elements having index > (N-1) are discarded
                               - last:     element (N-1) is the average of all elements having index > (N -1)
        :param cache_file: The cachefile containing a cached version of the similarity graph
        """

        self.N = N
        if transformation.lower() == 'truncate':
            self.transformation = self.__truncate_transformation
        elif transformation.lower() == 'avg':
            self.transformation = self.__average_transformation
        else:
            raise f"Unknown transformation: {transformation}, only 'truncate' or 'avg' are allowed"

        if not os.path.isfile( cache_file):
            self.__fill_cache( cache_file, Corpus(directory=corpus_dir),  DocumentVectors.read(documentvectors_dir))

        (self.data, self.labels) = self.__read_from_cache( cache_file)

    def __fill_cache(self, file, corpus, document_vectors):
        """
        Fill the cache if it does not exist
        :param file The cache file to be created
        :param corpus The corpus
        :param file The documentvectors
        """

        labels = []
        rows = []
        for pair in corpus.read_document_pairs():
            src = pair.get_src()
            dest = pair.get_dest()

            if document_vectors.documentvector_exists( src) and document_vectors.documentvector_exists( dest):
                src_vector = document_vectors.get_documentvector( pair.get_src())
                dest_vector = document_vectors.get_documentvector( pair.get_dest())

                src_vectors = [vector for (index, vector) in src_vector.get_sections()]
                dest_vectors = [vector for (index, vector) in dest_vector.get_sections()]
                distances = distance.cdist(src_vectors, dest_vectors, 'cosine')
                sim_matrix = 1 - distances

                vector = self.__matrix_to_vector( sim_matrix)
                rows.append( vector)

                labels.append( pair.get_similarity() )


        self.__save_in_pickle(rows, labels,  file)


    def __read_from_cache(self, file):
        """
        Read thy numpy arrays for data and labels from the file
        :param file:
        :return: (data, labels)
        """

        with open(file, "rb") as pickle_file:
            (data, labels) = pickle.load(pickle_file)

        return data, labels


    def __save_in_pickle(self, data, labels, file):
        """
        Saves the data and the labels in a pickle file
        :param data:
        :param file:
        :return: None
        """

        with open(file , "wb") as pickle_file:
            pickle.dump( (data, labels), pickle_file)


    def __matrix_to_vector(self, sim_matrix):
        """
        Converts the similarty matrix into a vector of size (matrix_rows) * (N)
        :param sim_matrix:
        :return:
        """

        rows = []
        columns = sim_matrix.shape[1]
        for row in sim_matrix:
            if columns == self.N:
                nw_vector = list( row)
            elif columns <= self.N:
                nw_vector = list(row) + ([0] * (self.N - columns))
            else:
                nw_vector = self.transformation( list( row))

            rows.append(nw_vector)

        list_of_zeros = [0] * (self.N)
        # now make sure we have only N vectors
        if len(rows) == self.N:
            vectors = rows
        elif len(rows) <= self.N:
            vectors = rows
            for i in range( len(rows), N):
                vectors.append( list_of_zeros)
        else:
            vectors = rows[0:self.N]

        # Flatten into a vector
        vector = []
        for vec in vectors:
            vector += vec

        return vector


    def __truncate_transformation(self, matrix_row):
        """
        Returns a vector of the matrix_row, that is larger than N
        :param matrix_row:
        :return:
        """

        return matrix_row[0:(self.N - 1)]

    def __average_transformation(self, matrix_row):
        """
        Returns a vector of the matrix_row, that is larger than N
        :param matrix_row:
        :return:
        """

        average = mean( matrix_row[(self.N - 1):])
        return matrix_row[0:(self.N - 1)] + [average]


    def __len__(self):
        """
        Standard functions that returns the number of documentpairs
        :return:
        """

        return len( self.data)


    def __getitem__(self, idx):
        """
        Get the i-th item from the dataset
        :param idx:
        :return:
        """

        return (self.data[idx], self.labels[idx])


#
# N = 12
# test_ds = SectionDataset( N=N, corpus_dir="/Volumes/Extern/Studie/studie/corpora/wikisim_nl", documentvectors_dir="/Volumes/Extern/Studie/studie/vectors/wikisim_nl.xml", transformation="avg", cache_file=f"/Volumes/Extern/Studie/studie/scratch/wikisim_nl/dataset_{N}.pkl")
# for (data, label) in test_ds:
#     print( f"{len(data)} :  {label}   :  {data[0]}  :  {data[N -1]}")