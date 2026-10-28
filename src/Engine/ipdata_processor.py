#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ipdata_processor.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/13 10:43:25 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/28 11:14:15 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os

from typing import List
from ..Base.model import path_dict, ChunkNode
# from .chunking import python_file_processor, md_txt_file_processor
from .md_text_chunking import md_txt_processor
from .python_chunking import python_processor
from .tokenizer import tokenization

def source_processor(max_chunk_size: int) -> None:
    """This is a inital point that divides the task,
     we do through every single file in raw folder
     and this is where the branching happens (like txt or py etc)"""
    # source_location: dict[str, List[int, int]] = {}
    chunk_data_list: list[ChunkNode] = []
    processed_files: list[str] = []
    temp_list = []
    for dirpath, dirnames, filenames in os.walk(
        "./" + path_dict("DATA_PATH")
    ):
        # ingest needed files
        for file in filenames:

            if (file.endswith(".txt") or file.endswith(".md")):
                file_path = os.path.join(dirpath, file)
                md_txt_processor(chunk_data_list,
                    file_path, max_chunk_size)
                processed_files.append(file_path)
            if (file.endswith(".py")):
                file_path = os.path.join(dirpath, file)
                python_processor(chunk_data_list,
                    file_path, max_chunk_size)
                processed_files.append(file_path)

    with open("output.txt", "w") as f:

        for i, obj in enumerate(chunk_data_list):
            f.write(f" \n\n ================================== \n\n [{i}]: {obj.file_path} \n {obj.text}, {obj.char_count}, {obj.start_index}, {obj.end_index}")
            if obj.char_count > max_chunk_size:
                print("########invalid_chunk######")
                break
            if obj.file_path not in temp_list:
                temp_list.append(obj.file_path)

    with open("filenames.txt", "w") as fn:

        for name in processed_files:
            fn.write(name + "\n")
    print(f" length of processed files: {len(temp_list)}")
    print(f" length of total files: {len(processed_files)}")
    for file in processed_files:
        if file not in temp_list:
            print(file)
    tokenization(chunk_data_list)

