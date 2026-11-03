#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   tokenizer.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/28 10:46:58 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/03 20:37:53 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from functools import lru_cache
from ..Base.model import Tokenized_data, MinimalSource
from transformers import AutoTokenizer, BertTokenizer
import tiktoken
import regex


def tokenize(text: str) -> list[str]:
    # step1: upper case to lower case
    text = text.lower()

    pattern1 = regex.compile(r"\p{L}+(?:['’]\p{L}+)*|\p{N}+(?:[.,]\p{N}+)*|[^\s]")
    word_list = pattern1.findall(text)

    pattern2 = r"\p{L}+?(?:ing|ed|tion|ly|ment)?|\p{N}+|[^\s]"
    pattern3 = r"'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+|\w+|ing|zation|ed"
    for word in word_list:
        if pattern2 in word:
            word_list.append(re.split(pattern2, word))

    @lru_cache(maxsize=None)
    def token_to_id(str):
        index = token_to_id.cache_info(currsize)
        return index        


def encode
def decode

def regex_tokenization



def tokenization(chunk_node_list):
    file_names = []
    tokenized_data: List[Tokenized_data] = []
    tokenizer = BertTokenizer.from_pretrained('Qwen/Qwen-7B', trust_remote_code=True)

    with open("processed", "w") as file_object:
        for unit in chunk_node_list:

            chunk = Tokenized_data(
                    tokenizer.encode(unit.text),
                    unit)

            tokenized_data.append(chunk)

            if unit.file_path not in file_names:
                file_object.write(f"\n{unit.file_path} \n {tokenizer.encode(unit.text)} \n")
                file_names.append(unit.file_path)
            else:
                file_object.write(f"{tokenizer.encode(unit.text)} \n")

    return tokenized_data
    # Must make it efficient by normailzation, but not for now.









# r"'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"


# def tokenization(chunk_node_list):
#     file_names = []
#     tokenized_data: List[Tokenized_data] = []
#     tokenizer = BertTokenizer.from_pretrained('Qwen/Qwen-7B', trust_remote_code=True)

#     with open("processed", "w") as file_object:
#         for unit in chunk_node_list:
#             # processed_data = unit.file_path, unit.char_start, unit.char_end, tokenizer.encode(unit.text)
#             chunk = Tokenized_data(
#                     tokenizer.encode(unit.text),
#                     unit)

#             tokenized_data.append(chunk)

#             if unit.file_path not in file_names:
#                 file_object.write(f"\n{unit.file_path} \n {tokenizer.encode(unit.text)} \n")
#                 file_names.append(unit.file_path)
#             else:
#                 file_object.write(f"{tokenizer.encode(unit.text)} \n")

#     return tokenized_data
#     # Must make it efficient by normailzation, but not for now.
