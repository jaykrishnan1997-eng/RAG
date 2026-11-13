#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 13:59:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/13 18:54:26 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import json
import argparse
from os import walk
from .model import (
    path_dict, UnansweredQuestion, RagDataset, MinimalSource, MinimalSearchResults, AnsweredQuestion, Givenanswers)



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
        "--answer_path", default=path_dict("ip_ans_path"))
    parser.add_argument(
        "--save_directory", default=path_dict("OUTPUT_PATH"))
    parser.add_argument(
        "--student_search_results_path", default=path_dict(
            "STUDENT_SEARCH_RESULTS_PATH"))
    return parser.parse_args()

# question loader


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


def input_datatset_loader(file_path, q_stat):

    if file_path.endswith('.json'):
        question_objects = json_loader(file_path)
        q_stat.stat[file_path] = len(question_objects)
    elif os.path.isdir(file_path):
        question_objects = []
        res = []
        for root, dir_names, file_names in os.walk(file_path):
            for file in file_names:
                if file.endswith('.json'):
                    res.append(os.path.join(root, file))
        for file1 in res:
            temp_questions = json_loader(file1)
            question_objects.extend(temp_questions)
            q_stat.stat[file1] = len(temp_questions)
    else:
        raise Exception('Unsupportable files provided')
    result = RagDataset()
    result.rag_questions = question_objects
    return question_objects

#  Given Answer loader


def ans_json_loader(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} file was not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in the file {file_path}")
    answer_objects = []
    answer_list = data["rag_questions"]

    for unit in answer_list:
        sources_list = []
        for s in unit["sources"]:
            sources_list.append[MinimalSource(
                file_path=s["file_path"],
                first_character_index=s["first_character_path"],
                last_character_index=s["last_character_index"]
            )]
        object = Givenanswers(
            queation_id=unit["question_id"],
            question=unit["question"],
            answer=unit["answer"],
            sources=sources_list,
        )
        answer_objects.append(object)
    return answer_objects


def answer_loader(file_path, answer_stat):

    if file_path.endswith('.json'):
        answer_objects = ans_json_loader(file_path)
        answer_stat.stat[file_path] = len(answer_objects)
    elif os.path.isdir(file_path):
        answer_objects = []
        res = []
        for root, dir_names, file_names in os.walk(file_path):
            for file in file_names:
                if file.endswith('.json'):
                    res.append(os.path.join(root, file))
        for file1 in res:
            temp_answers = ans_json_loader(file1)
            answer_objects.extend(temp_answers)
            answer_stat.stat[file1] = len(temp_answers)
    else:
        raise Exception('Unsupportable files provided')
    result = RagDataset()
    result.rag_questions = answer_objects
    return result
