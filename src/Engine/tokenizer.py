#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   tokenizer.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/28 10:46:58 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/28 11:32:49 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from transformers import AutoTokenizer
import tiktoken


def tokenization(chunk_node_list):
    processed_data = []
    file_names = []
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen-7B', trust_remote_code=True)

    with open("processed", "w") as file_object:
        for unit in chunk_node_list:
            # processed_data = unit.file_path, unit.char_start, unit.char_end, tokenizer.encode(unit.text)
            if unit.file_path not in file_names:
                file_object.write(f"\n{unit.file_path} \n {tokenizer.encode(unit.text)} \n")
                file_names.append(unit.file_path)
            else:
                file_object.write(f"{tokenizer.encode(unit.text)} \n")
