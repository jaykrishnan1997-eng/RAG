#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   retrieval.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/03 10:16:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/09 12:51:39 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import BM25
import math
from .tokenizer import tokenize, encode, decode
from ..Base.model import data, Document
from collections import Counter

# # corpus = BM25.load("filename", document_column="text")
# corpus = [
#     "a cat is a feline and likes to purr",
#     "a dog is the human's best friend and loves to play",
#     "a bird is a beautiful animal that can fly",
#     "a fish is a creature that lives in water and swims",
# ]

# retriever = BM25.index(corpus)
# breakpoint()
# queries = ["can dog fly", " what is a fish"]
# results = retriever.search(queries, k=5)

# for result in results[0]:
#     print(f"Score: {result['score']:.2f} | Document: {result['document']}")


class BM25_retrieval:
    def __init__(self, data, documents, question_nodes):
        self.documents = documents
        self.question_nodes = question_nodes

        self.document_length = {}
        self.term_frequency = {}
        self.document_frequency = Counter()

        self.query_score = []

        self.k1 = 0.5
        self.b = 0.75

        # compute document stats
        for document in documents:

            # collect all token_id from doc
            tokens = []

            for node in document.data_nodes:
                tokens.extend(node.tokens)

            # Document length
            self.document_length[document] = len(tokens)

            # term frequency for this document
            tf = Counter(tokens)
            self.term_frequency[document] = tf

            # document frequency: count each token once per document
            for keyword_id in tf:
                self.document_frequency[keyword_id] += 1

        # Calculate av doc length
        total_length = sum(self.document_length.values())

        if self.documents:
            self.avgl = total_length / len(self.documents)
        else:
            self.avgl = 0

        # Score every query
        for query in question_nodes:

            # Tokenise and encode each query once
            encoded_query = encode(data, tokenize(data, query.question))

            if not isinstance(encoded_query, list):
                encoded_query = [encoded_query]

            scores = [self.score(document, encoded_query) for document in documents]

            self.query_score.append(scores)

    def frequency(self, document, keyword_id):
        # how many times this keyword_id occured in the given document
        return self.term_frequency[document].get(keyword_id, 0)

    def IDF(self, keyword_id):
        n = 0
        tot_docs = len(self.documents)

        n = self.document_frequency.get(keyword_id, 0)
        idf = math.log(1 + (tot_docs - n + 0.5) / (n + 0.5))
        return idf

    def score(self, document, tokenized_query):

        score = 0

        doc_len = self.document_length[document]
        tf_dict = self.term_frequency[document]

        if self.avgl != 0:
            length_ratio = doc_len / self.avgl
        else:
            length_ratio = 0

        for keyword_id in tokenized_query:
            tf = tf_dict.get(keyword_id, 0)

            if tf == 0:
                continue
            idf = self.IDF(keyword_id)

            score += (idf * ((tf * (self.k1 + 1)))/(tf + self.k1 * (1 - self.b + (self.b * length_ratio))))
        return score


    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))