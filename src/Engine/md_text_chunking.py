#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   md_text_chunking.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/17 10:11:42 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/23 14:13:52 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

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


def md_txt_processor(
    chunk_data_list,
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a markdown file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""
    code_lines: str = ""
    end: int
    start_index: int = 0
    end_index: int = 0
    seperator: str

    with open(file_path, 'r', encoding='utf-8') as file_object:

        content = file_object.read()
    buffer = content
    if file_path.endswith(".md"):
        seperator = "\n\n---\n\n"
    else:
        seperator = "\n\n"
    while buffer != "":
        if seperator in buffer:
            end = buffer.index(seperator) + len(seperator)
        else:
            end = len(buffer)
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
