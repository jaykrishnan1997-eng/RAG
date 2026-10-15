#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   chunking.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/15 09:34:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/15 12:01:51 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import ast


def python_file_processing(file_path: str) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""

    first_character_index: int = 0
    last_character_index: int = 10

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()
        tree = ast.parse(content)
        print(ast.dump(tree, indent=4))
    return [first_character_index, last_character_index]
