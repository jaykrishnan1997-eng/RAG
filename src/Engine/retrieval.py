#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   retrieval.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/03 10:16:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/09 09:12:59 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import BM25
import math
from .tokenizer import tokenize, encode, decode
from ..Base.model import data, Document

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

        # length of tokens for every document
        length = 0
        for document in documents:
            for node in document.data_nodes:
                length += len(node.tokens)
            self.document_length[document] = length
            length = 0

        # for each query we have list of document scores
        # Q1 : [D1, D2, D3]; Q2: [D1, D2, D3]
        query_score: list[list[float]] = []
        document_score = []

        for query in question_nodes:
            query_score.append(
                [self.score(self.document_length, document, query) for document in documents])
        return query_score

    def frequency(self, document, keyword_id):
        # how many times this keyword_id occured in the given document
        occurance = 0
        for node in document.data_nodes:
            for token_id in node.token_list:
                if token_id == keyword_id:
                    occurance += 1
    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))

    def IDF(self, documents, keyword_id):
        n = 0
        tot_docs = len(documents)
        flag = 0
        for document in documents:
            for node in document.data_nodes:
                if keyword_id in node.tokens:
                    flag = 1
            n += flag
            flag = 0
        idf = math.log((tot_docs - n + 0.5) / (n + 0.5))
        return idf

    def score(self, document_length, document, query):
        score = 0
        total_length = 0
        tokenized_query = encode(data, tokenize(data, query.question))
        documents = document_length.keys()

        doc_len = document_length[document]
        for value in document_length.values():
            total_length += value
        avg = total_length / len(document_length)

        k1 = 0.5
        b = 0.75

        for keyword_id in tokenized_query:
            score += (self.IDF(documents, keyword_id) * ((frequency(document, keyword_id) * ( k1 + 1)))/(frequency(document, keyword_id) + k1 * ( 1 - b + (b * (doc_len / avg)))))
        return score
