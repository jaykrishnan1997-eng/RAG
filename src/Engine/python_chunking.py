#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   python_chunking.py                                   :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/15 09:34:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/23 13:55:02 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import ast
from ..Base.model import ChunkNode


def push(code_line, file_path, start_index, end_index):

    return (
        ChunkNode(
            code_line,
            file_path,
            len(code_line),
            start_index,
            end_index))


def split(
    chunk_data_list, code_lines,
    file_path, max_char,
    start_index, actual_end_index
):
    """Given a big chunk inside the markdown files,
    this function breaks it into smaller chunks"""
    overlap: int = int(0.15 * max_char)

    while code_lines != "":

        lines = code_lines[:max_char]
        code_lines = code_lines[(max_char - overlap):]
        end_index = start_index + max_char
        chunk_data_list.append(
                    push(lines, file_path, start_index, end_index))
        start_index += (max_char - overlap)
    return chunk_data_list


def python_processor(
    chunk_data_list,
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""
    temp_dict = {}
    code_lines: str = ""
    end: int
    start_index: int = 0
    end_index: int = 0
    seperator = [", body="]

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()

    tree = ast.parse(content)
    ast_content = ast.dump(tree)

    buffer = ast_content
    while buffer != "":
        code_lines = buffer[:end]
        end_index = start_index + end - 1
        if (end_index - start_index + 1) <= max_char:
            chunk_data_list.append(
                push(
                    code_lines, file_path,
                    start_index, end_index
                ))
        else:
            split(
                chunk_data_list, code_lines,
                file_path, max_char, start_index, end_index)
        start_index += end
        buffer = buffer[end:]

    # for obj in chunk_data_list:
    #     print(f"[{obj.text}]: {obj.start_index}, {obj.end_index} \n\n")

    return chunk_data_list



















# # from sentence_transformers import SentenceTransformer

# # # 1. Load a model that supports both text and images
# # model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")

# # # 2. Encode images from URLs
# # img_embeddings = model.encode([
# #     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
# #     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
# # ])

# # # 3. Encode text queries (one matching + one hard negative per image)
# # text_embeddings = model.encode([
# #     "A green car parked in front of a yellow building",
# #     "A red car driving on a highway",
# #     "A bee on a pink flower",
# #     "A wasp on a wooden table",
# # ])

# # # 4. Compute cross-modal similarities
# # similarities = model.similarity(text_embeddings, img_embeddings)
# # print(similarities)
# # # tensor([[0.5115, 0.1078],
# # #         [0.1999, 0.1108],
# # #         [0.1255, 0.6749],
# # #         [0.1283, 0.2704]])
