#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/06 12:42:35 by jkrishna           ###   ########.fr      #
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
from .Base.model import data, Documents
from .Engine.tokenizer import tokenize, encode, decode
from .Engine.retrieval import BM25_retrieval

# from transformers import AutoTokenizer

data = data()
bm25 = BM25_retrieval()
doc = Document()


def main() -> None:

    # parsing
    args = parse_args()

    # input data processing from vlllm # Chunking and cacheing
    tokenized_data_list = source_processor(data, args.max_chunk_size)
    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))

    # soring the documents
    documents = []
    for tokenized_data in tokenized_data_list:
        if tokenized_data
        doc()
    # writing an output with the vocab dict
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/file.json", "w", encoding="utf-8") as f:
        # json.dump(vocab_dict, f, indent=4)
        json.dump(data.index_list, f, indent=4)

    # creating and collecting the query_nodes
    question_nodes = input_datatset_loader(args.ip_unans_docs_path)

    # Collecting the documents and info on documents
    bm25(tokenized_data_list, question_nodes)


    # Embedding ?
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
