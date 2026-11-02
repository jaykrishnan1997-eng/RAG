#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/02 11:58:42 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import fire
import json
import tiktoken
import traceback
from .Base.parser import parse_args, input_datatset_loader
from .Engine.ipdata_processor import source_processor

from transformers import AutoTokenizer


def main() -> None:

    vocab_dict = {}
    # parsing
    args = parse_args()

    # input data processing from vlllm
    # Chunking and cacheing
    data_list = source_processor(args.max_chunk_size)
    tokenizer = AutoTokenizer.from_pretrained(
        'Qwen/Qwen-7B', trust_remote_code=True)
    for unit in data_list:
        for token in unit.tokens:
            vocab_dict[token] = tokenizer.decode(token)

    os.makedirs("data/output", exist_ok=True)
    # breakpoint()
    print(tokenizer.encode("tokenization").tokens)
    with open("data/output/file.json", "w", encoding="utf-8") as f:
        json.dump(vocab_dict, f, indent=4)
        # f.write(str(vocab_dict))
    # validating and accesing the input json file
    # rag_questions = input_datatset_loader(args.ip_unans_docs_path)
    # print(rag_questions)
    # Embedding
    # Retrieval
    # Generation using Qwen
    # fire.Fire("hello")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
