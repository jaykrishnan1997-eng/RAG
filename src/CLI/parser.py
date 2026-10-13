#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 13:59:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 09:36:49 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import argparse
from ..Base/model import Path_dict


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
        "--dataset_path", default=Path_dict.Path["ip_unans_docs_path"])
    parser.add_argument(
        "--save_directory", default=Path_dict.Path["op_path"])
    parser.add_argument(
        "--student_search_results_path", default=Path_dict.Path["op_path"])
    return parser.parse_args()



class Path_dict():
    Path = {
        "ip_ans_code_path":
        "data/datasets/AnsweredQuestions/dataset_code_public.json",
        "ip_ans_docs_path":
        "data/datasets/AnsweredQuestions/dataset_docs_public.json",
        "ip_unans_code_path":
        "data/datasets/UnansweredQuestions/dataset_code_public.json",
        "ip_unans_docs_path":
        "data/datasets/UnansweredQuestions/dataset_docs_public.json",
        "student_search_results_path":
        " data/output/search_results/UnansweredQuestions/dataset_docs_public.json",
        "op_path": "data/output/search_results/UnansweredQuestions",
        "processed_path": "data/datasets/processed",
        "vector_path": "data/datasets/vector"
    }
