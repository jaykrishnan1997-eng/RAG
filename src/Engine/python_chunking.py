#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   python_chunking.py                                   :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/15 09:34:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/10 10:55:49 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import ast
import sys
from ..Base.model import ChunkNode, push
from .md_text_chunking import split


def get_node_offsets(node, content_lines):
    start_line = content_lines[node.lineno - 1]
    end_line = content_lines[node.end_lineno - 1]

    start_index = (
        sum(len(line) for line in content_lines[:node.lineno - 1])
        + len(start_line.encode("utf-8")[:node.col_offset].decode("utf-8"))
    )

    end_index = (
        sum(len(line) for line in content_lines[:node.end_lineno - 1])
        + len(end_line.encode("utf-8")[:node.end_col_offset].decode("utf-8"))
        - 1
    )
    return start_index, end_index


def line_char_dict(content_line):
    # dictionary of line_number: [start_char_index, end_char_index]
    line_dict = {}
    line_start_char = 0
    # content_copy = content
    for i, line in enumerate(content_line):
        line_dict[i + 1] = [line_start_char, (line_start_char + len(line) - 1)]
        line_start_char += len(line)
    return line_dict


def recursive_splitter(tree, temp_list, file_path, max_char, content):
    node_list = tree.body if hasattr(tree, 'body') else [tree]

    for node in node_list:
        code_line = ast.get_source_segment(content, node)

        if len(code_line) > max_char and hasattr(node, 'body'):
            sub_tree = ast.Module(body=node.body, type_ignore=[])
            recursive_splitter(sub_tree, temp_list, file_path, max_char, line_dict)
        else:
            # Leaf node that's too long - emit as-it-is
            start_index, end_index = get_node_offsets(node, content_lines)
            original_segment = content[start_index:end_index + 1]

            if original_segment != code_line:
                print("OFFSET MISMATCH!")
                print("AST segment:", repr(code_line))
                print("Source segment:", repr(original_segment))
                print("Start:", start_index, "End:", end_index)
            temp_list.append(
                push(code_line, file_path, start_index, end_index))
    return (temp_list)


def python_flush(temp_list, merged_list):
    new_text = ""

    for unit in temp_list:
        if new_text != "":
            # new_text += "\n" + unit.text
            new_text += unit.text
        else:
            new_text = unit.text
    merged_list.append(push(
        new_text, temp_list[0].file_path,
        temp_list[0].start_index, temp_list[-1].end_index))
    temp_list = []
    return merged_list


def merger(chunk_list, max_char):
    i = 0
    merged_list = []
    temp_list = []
    total_char_count = 0
    # breakpoint()
    while i < len(chunk_list):

        while (total_char_count + len(chunk_list[i].text)) < max_char:
            total_char_count += len(chunk_list[i].text)
            temp_list.append(chunk_list[i])
            i += 1

            if (i < len(chunk_list)) and ((total_char_count + len(chunk_list[i].text)) >= max_char):
                python_flush(temp_list, merged_list)
                temp_list = []
                total_char_count = 0

            if i >= len(chunk_list):
                if temp_list != []:
                    python_flush(temp_list, merged_list)
                break

        if (i < len(chunk_list)) and (len(chunk_list[i].text) >= max_char):
            split(temp_list, chunk_list[i].text, chunk_list[i].file_path, max_char, chunk_list[i].start_index, chunk_list[i].end_index)
            for unit in temp_list:
                merged_list.append(unit)
            temp_list = []
            total_char_count = 0
            i += 1

    return (merged_list)


def python_processor(
    chunk_data_list,
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()

    content_lines = content.splitlines(keepends=True)

    if len(content) <= max_char:
        chunk_data_list.append(push(content, file_path, 0, len(content) - 1))
        return (chunk_data_list)

    # breakpoint()
    tree = ast.parse(content, type_comments=True)

    try:
        broken_chunk_data_list = recursive_splitter(
            tree, [], file_path, max_char, content)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)
    # print(broken_chunk_data_list)
    for unit in merger(broken_chunk_data_list, max_char):

        if isinstance(unit, ChunkNode):
            chunk_data_list.append(unit)
        else:
            for sub_unit in unit:
                chunk_data_list.append(sub_unit)

    # for obj in chunk_data_list:
    #     print(f"[{obj.text}]: {obj.start_index}, {obj.end_index}, chunk_size = {obj.char_count} \n\n")
    return chunk_data_list
