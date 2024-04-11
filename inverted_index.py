from math import log10
import logging

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.idf = {}
        self.no_of_documents = 0
        self.document_term_frequency = {}
        self.document_token_length = {}
        self.DAMPING_FACTOR = 0.001

        # Set logging config
        logging.basicConfig(
            format="%(asctime)s, %(levelname)s, %(funcName)s, %(pathname)s, %(message)s", level=logging.DEBUG)

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
            idf = log10(self.no_of_documents /
                        (1 + no_of_document_that_have_token)) + 1
            return idf
        except Exception as e:
            logging.debug("Error calculating idf")
            return self.DAMPING_FACTOR

    def calculate_tf(self, token, document):
        try:
            token_frequency = self.document_term_frequency[document][token]
            document_token_length = self.document_token_length[document]

            return token_frequency / document_token_length
        except Exception as e:
            logging.debug("Token: %s not in Document: %s", token, document)
            return self.DAMPING_FACTOR

    def calculate_tf_idf(self, document, token):
        tf = self.calculate_tf(token=token, document=document)
        idf = self.calculate_idf(token)
        return tf * idf

    def get_document_tf_idf_score(self, document, query_tokens):
        tf_idf_scores = []
        total_idf_score = 1
        for query in query_tokens:
            tf_idf = self.calculate_tf_idf(
               document=document, token=query)
            tf_idf_scores.append((query, tf_idf))
            total_idf_score *= tf_idf

        logging.debug("TF - IDF scores for query: %s is %f",
                      str(query_tokens), total_idf_score)

        return total_idf_score
    
    def rank_results(self, results):
        return sorted(results, key=lambda x: x[1], reverse=True)

    def search(self, query):
        query_tokens = query.split()

        documents_to_search = set()


        for query_token in query_tokens:
            documents_to_search = documents_to_search.union(self.index[query_token])

        results = []

        for document in documents_to_search:
            result = (document, self.get_document_tf_idf_score(
                document=document, query_tokens=query_tokens))
            results.append(result)

        ranked_results = self.rank_results(results=results)

        return ranked_results
