#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   retrieval.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/03 10:16:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/03 11:39:50 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import BM25

# corpus = BM25.load("filename", document_column="text")
corpus = [
    "a cat is a feline and likes to purr",
    "a dog is the human's best friend and loves to play",
    "a bird is a beautiful animal that can fly",
    "a fish is a creature that lives in water and swims",
]

retriever = BM25.index(corpus)
breakpoint()
queries = ["can dog fly", " what is a fish"]
results = retriever.search(queries, k=5)

for result in results[0]:
    print(f"Score: {result['score']:.2f} | Document: {result['document']}")
