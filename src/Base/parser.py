#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 13:59:36 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/16 12:45:06 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import argparse
from .model import path_dict


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
        "--dataset_path", default=path_dict("ip_unans_docs_path"))
    parser.add_argument(
        "--save_directory", default=path_dict("OUTPUT_PATH"))
    parser.add_argument(
        "--student_search_results_path", default=path_dict(
            "STUDENT_SEARCH_RESULTS_PATH"))
    return parser.parse_args()
