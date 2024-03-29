# Class for the sent2Vec encoder
import os

import sent2vec

import functions
from texts.clean import Cleaner

from documentencoders.documentencoder import Documentencoder_base


class Sent2VecEncoder(Documentencoder_base):

    SENT2VECMODELPATH = "Pretrained/Sent2Vec/wiki_unigrams.bin"
    SENT2VECVECTORSIZE = 600

    def __init__(self, language_code):
        super(Sent2VecEncoder, self).__init__(language_code)

        modelpath = os.path.join(os.getcwd(), Sent2VecEncoder.SENT2VECMODELPATH)
        self.sent2vec = sent2vec.Sent2vecModel()
        self.sent2vec.load_model(modelpath)

        self.cleaner = Cleaner(language_code=self.language_code)

    def get_vector_size(self):
        """
        The resulting vector size
        :return:
        """
        return Sent2VecEncoder.SENT2VECVECTORSIZE      # This is because the Pretrained model has a fixed vector size


    def embed_text(self, text):
        """
        Create sentence to vec embedding
        :param text: can either be a string or a list of strings (sentences)
        :return:
        """

        joined = " ".join( text) if type(text) == list else text
        clean = self.cleaner.clean_text(txt=joined, remove_stop=True, remove_digits=True, lower=False)
        vector = self.sent2vec.embed_sentence( " ".join(clean))

        return vector[0]            # return the first vector (there is only one)
