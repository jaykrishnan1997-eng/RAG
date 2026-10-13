#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 13:59:13 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import fire
from Base.parser import parse_args
from Engine.ipdata_processor import source_processor


# def hello(name):
#     return f'Hello {name}!'


def main() -> None:
    # parsing
    args = parse_args()

    # input data processing from vlllm
    source_processor()
    # Chunking and cacheing
    # Embedding
    # Retrieval
    # Generation using Qwen  
  
    # fire.Fire("hello")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception caught: {e}")
        sys.exit(1)
