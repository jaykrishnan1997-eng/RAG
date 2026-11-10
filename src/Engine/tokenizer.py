#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   tokenizer.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/28 10:46:58 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/10 12:49:12 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from ..Base.model import Tokenized_data, MinimalSource, data, Document
# from transformers import AutoTokenizer, BertTokenizer
# import tiktoken
import regex

# data = data()


def tokenize(data, text: str) -> list[str]:

    # split camelCase / PascalCase, then lower case
    text = regex.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = regex.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    text = text.lower()

    word_list = []
    pattern1 = regex.compile(r"\p{L}+|\p{N}+(?:[.,]\p{N}+)*|[^\s]")
    word_list = pattern1.findall(text)

    # pattern2 = r'\p{L}+?(?:ing|ed|tion|ly|ment|ization)?|\p{N}+|[^\s]'
    divider = [
        "ing", "ed", "tion", "ly", "ment", "ization",
        "ness", "ity", "ism", "ist", "ance", "ence",
        "ure", "ary", "ory", "sion", "ation", "hood", "ship",
        "ous", "ful", "less", "able", "ible", "al",
        "ic", "ive", "ish", "en",
        "ify", "ize", "ise", "ate",
        ]
    # pattern3 = r"'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+|\w+|ing|zation|ed"

    noice_words = [
        "a", "an", "the", "is", "are", "were", "was", "an", "be",
        "been", "and", "or", "but", "of", "at", "by", "from", "with"
    ]
    if word_list == [] and isinstance(text, str):
        if text not in noice_words:
            word_list.append(text)
        # word_list.append(text)
    result = []
    for word in word_list:
        for suffix in divider:

            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if len(stem) >= 3:
                    result.append(stem)
                # prefix = word.split(suffix)[0]
                # if len(prefix) >= 3:
                #     result.append(prefix)
                #     result.append(suffix)
    STOP = set(noice_words) | {
        "what", "which", "when", "does", "do", "how", "in", "to", "for",
        "on", "it", "its", "as", "this", "that", "if", "when", "default",
        "value", "vllm",
    }
    result = word_list + result
    return [t for t in result
            if t and t[0].isalnum() and t not in STOP
            and (len(t) > 1 or t.isdigit())]


# +    STOP = set(noice_words) | {
# +        "what", "which", "when", "does", "do", "how", "in", "to", "for",
# +        "on", "it", "its", "as", "this", "that", "if", "when", "default",
# +        "value", "vllm",
# +    }
#      result = word_list + result
# -    return result
# +    return [t for t in result if (t[0].isalnum()) and t not in STOP]

def encode(data, tokens: str | list[str]):
    #  given a token or list of token find the corresponding index
    if isinstance(tokens, list):
        token_list = []
        for token in tokens:
            token_list.append(data.add_token(token))
        return token_list
    else:
        return data.add_token(tokens)


def decode(data, ids: int | list[int]):
    if isinstance(ids, list):
        return [data.id_to_str(id) for id in ids]
    else:
        return data.id_to_str(ids)


def tokenization(data, chunk_node_list):
    file_names = []
    tokenized_data: list[Tokenized_data] = []

    with open("processed", "w") as file_object:
        for unit in chunk_node_list:

            chunk = Tokenized_data(encode(data, tokenize(data, unit.text)), unit)

            tokenized_data.append(chunk)

            if unit.file_path not in file_names:
                file_object.write(f"\n{unit.file_path} \n {encode(data, tokenize(data, unit.text))} \n")
                file_names.append(unit.file_path)
            else:
                file_object.write(f"{encode(data, tokenize(data, unit.text))} \n")

    return tokenized_data
    # Must make it efficient by normailzation, but not for now.


def document_sort(document_names, tokenized_data_list):

    documents = []
    data_nodes = []
    for doc_name in document_names:
        for item in tokenized_data_list:
            if item.source.file_path == doc_name:
                data_nodes.append(item)
        documents.append(Document(doc_name, data_nodes))
        data_nodes = []

    return documents
