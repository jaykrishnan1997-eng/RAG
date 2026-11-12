#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 13:59:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/12 13:45:45 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import json
import argparse
from os import walk
from .model import path_dict, UnansweredQuestion, RagDataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        "--max_chunk_size", default=2000)
    parser.add_argument(
        "--max_context_length", default=2000)
    parser.add_argument(
        "--k", default=5)
    parser.add_argument(
        "--dataset_path", default=path_dict("ip_unans_path"))
    parser.add_argument(
        "--save_directory", default=path_dict("OUTPUT_PATH"))
    parser.add_argument(
        "--student_search_results_path", default=path_dict(
            "STUDENT_SEARCH_RESULTS_PATH"))
    return parser.parse_args()


def json_loader(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} file was not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in the file {file_path}")
    question_objects = []
    question_list = data["rag_questions"]

    for unit in question_list:
        object = UnansweredQuestion(
            queation_id=unit["question_id"],
            question=unit["question"],
        )
        question_objects.append(object)
    return question_objects


def input_datatset_loader(file_path):

    if file_path.endswith('.json'):
        question_objects = json_loader(file_path)
    elif os.path.isdir(file_path):
        question_objects = []
        res = []
        for root, dir_names, file_names in os.walk(file_path):
            for file in file_names:
                if file.endswith('.json'):
                    res.append(os.path.join(root, file))
        for file in res:
            question_objects.extend(json_loader(file))
    else:
        raise Exception('Unsupportable files provided')
    return question_objects
