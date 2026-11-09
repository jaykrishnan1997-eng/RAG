#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/09 10:04:26 by jkrishna           ###   ########.fr      #
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
from .Base.model import data, Document
from .Engine.tokenizer import tokenize, encode, decode, document_sort
from .Engine.retrieval import BM25_retrieval

# from transformers import AutoTokenizer

data = data()



def main() -> None:

    # parsing
    args = parse_args()

    # input data processing from vlllm # Chunking and cacheing
    tokenized_data_list = source_processor(data, args.max_chunk_size)

    # soring the documents, return a document object
    documents = document_sort(data.documents, tokenized_data_list)

    # writing an output with the vocab dict
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/file.json", "w", encoding="utf-8") as f:
        # json.dump(vocab_dict, f, indent=4)
        json.dump(data.index_list, f, indent=4)

    # creating and collecting the query_nodes
    # currently i am only loading the docs not the python files

    question_nodes = input_datatset_loader(args.dataset_path)

    # # trial starts

    # print(encode(data, tokenize(data, "tokenization is a great thing")))
    # print(decode(data, encode(data, tokenize(data, "tokenization is a great thing"))))
    # # trial ends

    # Collecting the documents and info on documents
    bm25 = BM25_retrieval(data, documents, question_nodes)
    print(bm25)


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


    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))