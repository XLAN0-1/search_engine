from math import log10
import logging


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.idf = {}
        self.no_of_documents = 0
        self.document_term_frequency = {}
        self.document_token_length = {}
        self.DEFAULT_NULL_VALUE = 0.001
        # Set logging config
        logging.basicConfig(
            format="%(asctime)s, %(levelname)s, %(funcName)s, %(pathname)s, %(message)s", level=logging.INFO)

    def add_document(self, document, tokens):
        self.no_of_documents += 1
        token_count = {}
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()

            if token not in token_count:
                token_count[token] = 0
            token_count[token] += 1
            self.index[token].add(document)

        self.document_term_frequency[document] = token_count
        self.document_token_length[document] = len(tokens)

    def calculate_idf(self, token):
        try:
            no_of_document_that_have_token = len(self.index[token])
            idf = log10(self.no_of_document /
                        (1 + no_of_document_that_have_token)) + 1
            return idf
        except Exception as e:
            logging.debug("Error calculating idf")
            return self.DEFAULT_NULL_VALUE

    def calculate_tf(self, token, document):
        try:
            token_frequency = self.document_term_frequency[document][token]
            document_token_length = self.document_token_length[document]

            return token_frequency / document_token_length
        except Exception as e:
            logging.debug("Token: %s not in Document: %s", token, document)
            return self.DEFAULT_NULL_VALUE

    def calculate_tf_idf(self, document, token):
        tf = self.calculate_tf(token=token, document=document)
        idf = self.calculate_idf(token)
        return tf * idf

    def search(self, query):
        query_tokens = query.split()

        documents_to_search = set()

        for query_token in query_tokens:
            documents_to_search.union(self.index[query_token])
