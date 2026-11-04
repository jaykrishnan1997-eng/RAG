#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/04 14:02:40 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import fire
import json
# import tiktoken
import traceback
from .Base.parser import parse_args, input_datatset_loader
from .Engine.ipdata_processor import source_processor
from .Base.model import data
from .Engine.tokenizer import tokenize, encode, decode

# from transformers import AutoTokenizer

data = data()


def main() -> None:

    vocab_dict = {}
    # parsing
    args = parse_args()

    # input data processing from vlllm
    # Chunking and cacheing
    data_list = source_processor(data, args.max_chunk_size)

    # for unit in data_list:
    #     for token in unit.tokens:
    #         vocab_dict[token] = decode(data, token)

    os.makedirs("data/output", exist_ok=True)
    # breakpoint()
    print(encode(data, tokenize(data, "tokenization")))
    print(decode(data, encode(data, tokenize(data, "tokenization"))))
    # print(tokenizer.decode(5839))
    # print(tokenizer.decode(2022))
    with open("data/output/file.json", "w", encoding="utf-8") as f:
        # json.dump(vocab_dict, f, indent=4)
        json.dump(data.index_list, f, indent=4)
        # f.write(data.id_to_str)



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
