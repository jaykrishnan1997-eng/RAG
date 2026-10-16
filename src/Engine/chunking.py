#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   chunking.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/15 09:34:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/16 15:04:29 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from sentence_transformers import SentenceTransformer, util

import ast
import nltk
nltk.download('punkt_tab')


def python_chunking(
    text: str, max_tokens: int, model_name='all-MiniLM-L6-v2'
):
    """AST based recursive split and merge chunking statergy
     specific to python files"""
    chunks = []
    current_chunk = []
    seperators = [
        "\nclass",  # Class definition
        "\ndef",    # Function definition
        "\n\tdef",  # Method definition
        "\n\n",     # Blank lines(logical blocks)
        "\n",       # Lines
        " ",        # Words
        ""          # Characters
    ]
    current_tok_len = 0
    current_embedding = None

    model = SentenceTransformer(model_name)
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    for i, sentence in enumerate(sentences):
        sentence_tok_len = len(sentence.split())
        if current_tok_len + sentence_tok_len <= max_tokens:
            current_tok_len += sentence_tok_len
            current_chunk.append(sentence)
            if current_embedding is None:
                current_embedding = embeddings[i]
            else:
                current_embedding = util.pytorch_cos_sim(
                    current_embedding, embeddings[i]).mean()
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_tok_len = sentence_tok_len
            current_embedding = embeddings[i]
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def python_file_processor(
    file_path: str, last_character_index: int,
    max_tokens: int,
) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""

    first_character_index: int = 0

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()
        tree = ast.parse(content)
    # Using fixed size chunking for python files
    chunks = python_chunking(ast.dump(tree, indent=4), max_tokens)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        breakpoint()
    return [first_character_index, last_character_index]


def md_txt_chunking(
    text: str, max_tokens: int, model_name='all-MiniLM-L6-v2'
):
    """AST based recursive split and merge chunking statergy
     specific to python files"""
    chunks = []
    current_chunk = []
    md_seperators = [
        "\n##",     # H2 headers (major sections)
        "\n###",    # H3 headers (subsections)
        "\n####",   # H4 headers
        "\n\n",     # Paragraphs
        "\n",       # Lines
        ". ",       # Sentences
        " ",        # Words
        ""          # Characters
    ]
    txt_seperators = [
        "\n\n",     # Blank lines(logical blocks)
        "\n",       # Lines
        ". ",       # Words
        " ",        # Words
        ""          # Characters
    ]
    current_tok_len = 0
    current_embedding = None

    model = SentenceTransformer(model_name)
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    for i, sentence in enumerate(sentences):
        sentence_tok_len = len(sentence.split())
        if current_tok_len + sentence_tok_len <= max_tokens:
            current_tok_len += sentence_tok_len
            current_chunk.append(sentence)
            if current_embedding is None:
                current_embedding = embeddings[i]
            else:
                current_embedding = util.pytorch_cos_sim(
                    current_embedding, embeddings[i]).mean()
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_tok_len = sentence_tok_len
            current_embedding = embeddings[i]
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def md_txt_file_processor(
    file_path: str, last_character_index: int,
    max_tokens: int,
) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""

    first_character_index: int = 0

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()
        tree = ast.parse(content)
    # Using fixed size chunking for python files
    chunks = python_chunking(ast.dump(tree, indent=4), max_tokens)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        breakpoint()
    return [first_character_index, last_character_index]



























# from sentence_transformers import SentenceTransformer

# # 1. Load a model that supports both text and images
# model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")

# # 2. Encode images from URLs
# img_embeddings = model.encode([
#     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
#     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
# ])

# # 3. Encode text queries (one matching + one hard negative per image)
# text_embeddings = model.encode([
#     "A green car parked in front of a yellow building",
#     "A red car driving on a highway",
#     "A bee on a pink flower",
#     "A wasp on a wooden table",
# ])

# # 4. Compute cross-modal similarities
# similarities = model.similarity(text_embeddings, img_embeddings)
# print(similarities)
# # tensor([[0.5115, 0.1078],
# #         [0.1999, 0.1108],
# #         [0.1255, 0.6749],
# #         [0.1283, 0.2704]])