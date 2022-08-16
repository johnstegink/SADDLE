# Class that contains functionality for computing the distance
import numpy as np

from Distances.DocumentRelations import DocumentRelations
from annoy import AnnoyIndex
from scipy.spatial import distance as spdistance

NUMBEROFTREES = 50

class DistanceIndex:
    def __init__(self, documentvectors):
        self.documentvectors = documentvectors
        self.index = AnnoyIndex( documentvectors.get_vector_size(), "angular")
        self.index_to_id = {}
        self.id_to_index = {}
        self.search_k_multiply = 2

    def build(self):
        """
        Build the index based on the documentvectors
        :return:
        """

        i = 0
        for dv in self.documentvectors:
            id = dv.get_id()
            self.index_to_id[i] = id
            self.id_to_index[id] = i
            self.index.add_item(i, dv.get_vector())
            i += 1

        self.index.build(NUMBEROFTREES)


    def calculate_relations(self, minimal_similarity, nearest_lim=2, second_index=None):
        """
        Determine the relations between the documents given the minimal distance
        :param minimal_similarity: value between 0 and 1
        :param second_index: The name of the index to compare to, if ommitted the index is compared to itself
        :param nearest_lim: Limit
        :return: a object with document relations
        """

        dr = DocumentRelations()
        index_to_compare_to = second_index if not second_index is None else self

        for dv in self.documentvectors:
            src_id = dv.get_id()
            vector = np.array( dv.get_vector())
            src_index = self.id_to_index[src_id]

            (dest_indexes, distances) = index_to_compare_to.index.get_nns_by_vector(vector,n=nearest_lim + 1, search_k=(nearest_lim + 1)* self.search_k_multiply, include_distances=True)
            similarities = 1.0 - np.array( distances)

            added = 0
            for (dest_index, similarity) in zip( dest_indexes, similarities):
                if similarity > 0  and (second_index is None or dest_index != src_index):
                    if( float(similarity) >= minimal_similarity) and added < nearest_lim:
                        added += 1
                        dr.add(src=src_id, dest=index_to_compare_to.index_to_id[dest_index], distance=float(similarity))

        return dr


    def cosine_sim(self, id1, id2):
        """
        Calculate the cosine similarity
        :param id1:
        :param id2:
        :return:
        """
        vector1 = self.documentvectors.get_documentvector(id1).get_vector()
        vector2 = self.documentvectors.get_documentvector(id2).get_vector()

        return 1. / (1. + spdistance.cosine(vector1, vector2))