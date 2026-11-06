#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   retrieval.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/03 10:16:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/06 15:18:02 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import BM25
import math

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
        # for each query we have list of document scores
        # Q1 : [D1, D2, D3]; Q2: [D1, D2, D3]
        query_score: list[list[float]] = []
        document_score = []

        for query in question_nodes:
            query_score.append(
                [score(documents, document, query) for document in documents])

    def frequency(document, keyword_id):
        occurance = 0
        keyword_id = 
    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))

    def IDF(documents, keyword_id):
        n = 0
        tot_docs = len(documents)
        flag = 0
        for document in documents:
            for node in document.data_nodes
                if keyword_id in node.tokens:
                    flag = 1
            n += flag
            flag = 0
        idf = math.log((tot_docs - n + 0.5) / (n + 0.5))
                    
    def score(documents, document, query):
        score = 0
        tokenized_query = encode(data, tokenize(data, query.question))
        
        doc_len = 
        avg =

        k1 = 
        b = 
        
        for keyword_id in tokenized_query:
            score += (IDF(documents, keyword_id) * ((frequency(document, keyword_id) * ( k1 + 1)))/(frequency(document, keyword_id) + k1 * ( 1 - b + (b * (doc_len / avg)))))
    