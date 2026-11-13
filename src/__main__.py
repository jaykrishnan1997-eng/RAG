#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/13 18:11:13 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import fire
import json
# import tiktoken
import traceback
from .Base.parser import parse_args, input_datatset_loader, answer_loader
from .Engine.ipdata_processor import source_processor
from .Base.model import data, Document, Question_stat
from .Engine.tokenizer import tokenize, encode, decode, document_sort
from .Engine.retrieval import BM25_retrieval



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
    # loading the docs and the python files
    # Both the question nodes and answer nodes are loaded for recall and comparison


    question_stat = Question_stat()
    answer_stat = Question_stat()

    question_nodes = input_datatset_loader(args.dataset_path, question_stat)
    print(q_stat.stat)
    given_answer_nodes = answer_loader(args.answer_path, answer_path)
    # # trial starts

    # print(encode(data, tokenize(data, "tokenization is a great thing")))
    # print(decode(data, encode(data, tokenize(data, "tokenization is a great thing"))))
    # # trial ends

    # Retrieval: using bm25 get the node_score and node
    # bm25 returns scores and 
    bm25 = BM25_retrieval(data, documents, question_nodes)

    for k in range(0, 1):
        result = bm25.query_score[k]
        print(f"--- question {k} ---")

        for rank, (score, node) in enumerate(result[:10]):
            print(rank, round(score, 3), node.source.file_path,
                node.source.first_character_index,
                node.source.last_character_index)
            # print(node.text)
    
    # # :
    # expected = [
    #     ("vllm/model_executor/layers/fused_moe/fused_batched_moe.py", 28416, 28975),
    #     ("vllm/attention/ops/triton_flash_attention.py", 13507, 13600),
    #     ("vllm/model_executor/layers/sampler.py", 27480, 28492),
    #     ("vllm/entrypoints/llm.py", 64076, 64088),
    #     ("vllm/worker/model_runner.py", 64028, 64925),
    # ]
    # for k, (path, s, e) in enumerate(expected):
    #     for rank, (score, node) in enumerate(bm25.query_score[k]):
    #         src = node.source
    #         if (src.file_path.endswith(path)
    #                 and src.first_character_index <= e
    #                 and src.last_character_index >= s):
    #             print(k, "found at rank", rank)
    #             break
    #     else:
    #         print(k, "not found at all")

    # print("TOKENIZE V3")
    # q = "What's the default value of trust_remote_code in vLLM's LLM class constructor?"
    # print(tokenize(data, q))

    # path, s, e = "vllm/entrypoints/llm.py", 64076, 64088
    # for rank, (score, node) in enumerate(bm25.query_score[3]):
    #     src = node.source
    #     if (src.file_path.endswith(path)
    #             and src.first_character_index <= e
    #             and src.last_character_index >= s):
    #         print("rank", rank, src.first_character_index, src.last_character_index)
    #         print(repr(node.source_text if hasattr(node, "source_text") else ""))
    #         break

    # with open("data/raw/vllm-0.10.1/vllm/entrypoints/llm.py", encoding="utf-8") as f:
    #     print(repr(f.read()[s:e + 1]))

    # raw = open("data/raw/vllm-0.10.1/vllm/entrypoints/llm.py", "rb").read()
    # print(repr(raw[64076:64089].decode("utf-8", errors="replace")))
    # print(raw.count(b"trust_remote_code"))
    # print(len(raw) - len(raw.decode("utf-8")))  # > 0 means non-ASCII shifts offsets

    # txt = raw.decode("utf-8")
    # i = txt.find("trust_remote_code: bool")
    # print(i, repr(txt[i:i+60]))
    # #  END

    

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