#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ipdata_processor.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/13 10:43:25 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/21 10:18:28 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os

from typing import List
from ..Base.model import path_dict, MarkdownChunk
# from .chunking import python_file_processor, md_txt_file_processor
from .md_text_chunking import md_txt_processor


def source_processor(max_chunk_size: int) -> None:
    """This is a inital point that divides the task,
     we do through every single file in raw folder
     and this is where the branching happens (like txt or py etc)"""
    # source_location: dict[str, List[int, int]] = {}
    markdown_list: list[MarkdownChunk] = []

    for dirpath, dirnames, filenames in os.walk(
        "./" + path_dict("DATA_PATH")
    ):
        # ingest needed files
        for file in filenames:
            # if file.endswith(".py"):
            #     file_path = os.path.join(dirpath, file)
            #     source_location[file_path] = python_file_processor(file_path, last_character_index, max_chunk_size)
            #     last_character_index = source_location[file_path][1]
            if (file.endswith(".txt") or file.endswith(".md")):
                file_path = os.path.join(dirpath, file)
                md_txt_processor(markdown_list,
                    file_path, max_chunk_size)

    for obj in markdown_list:
        print(obj.file_path)
        print(obj.char_count, obj.start_index, obj.end_index)



    # elif file.endswith(".yaml"):
    #     print()

    # elif file.endswith(".sh"):
    #     print()

    # elif file.endswith(".json"):
    #     print()

    # elif file.endswith(".jinja"):
    #     print()
    # else:
    #     print(file)


    # # for obj in markdown_list:
    # print(markdown_list[2].char_count, markdown_list[2].start_index, markdown_list[2].end_index)
    # print(markdown_list[2].text)
    # print(markdown_list[2].file_path)
    # print(len(markdown_list[2].text))