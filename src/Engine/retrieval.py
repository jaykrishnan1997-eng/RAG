#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   retrieval.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/03 10:16:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/10 09:22:49 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import BM25
import math
from .tokenizer import tokenize, encode, decode
from ..Base.model import data, Document
from collections import Counter


class BM25_retrieval:
    def __init__(self, data, documents, question_nodes):
        self.documents = documents
        self.question_nodes = question_nodes

        self.node_stats = {}
        self.document_frequency = Counter()

        self.k1 = 0.5
        self.b = 0.75
        total_length = 0
        total_nodes = 0
        # compute document stats
        for document in documents:
            for node in document.data_nodes:

                tokens = node.tokens
                tf = Counter(tokens)
                node_length = len(tokens)

                self.node_stats[id(node)] = {
                    "length": node_length,
                    "tf": tf
                }

                # document frequency: count each token once per chunk
                for token_id in tf:
                    self.document_frequency[token_id] += 1

                # Calculate av doc length
                total_length += node_length
                total_nodes += 1

        if total_nodes:
            self.avgl = total_length / total_nodes
        else:
            self.avgl = 0

        # Score every query
        self.query_score = []

        for query in question_nodes:

            # Tokenise and encode each query once
            encoded_query = encode(data, tokenize(data, query.question))

            if not isinstance(encoded_query, list):
                encoded_query = [encoded_query]

            scores = []

            for document in self.documents:
                for node in document.data_nodes:

                    node_score = self.score(node, encoded_query)

                    if node_score > 0:
                        scores.append((node_score, node))

            scores.sort(key=lambda item: item[0], reverse=True)

            self.query_score.append(scores)

    def IDF(self, keyword_id):
        tot_docs = len(self.node_stats)

        n = self.document_frequency.get(keyword_id, 0)
        idf = math.log(1 + (tot_docs - n + 0.5) / (n + 0.5))
        return idf

    def score(self, node, tokenized_query):
        score = 0
        stats = self.node_stats[id(node)]

        node_length = stats["length"]
        tf_dict = stats["tf"]

        if self.avgl != 0:
            length_ratio = node_length / self.avgl
        else:
            length_ratio = 0

        idf_values = {
            keyword_id: self.IDF(keyword_id)
            for keyword_id in set(tokenized_query)
        }
        for keyword_id in tokenized_query:
            tf = tf_dict.get(keyword_id, 0)

            if tf == 0:
                continue

            idf = idf_values[keyword_id]

            score += (idf * ((tf * (self.k1 + 1)))/(tf + self.k1 * (1 - self.b + (self.b * length_ratio))))
        return score


    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))
