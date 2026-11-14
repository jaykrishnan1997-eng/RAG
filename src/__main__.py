#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/14 21:12:14 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import fire
import json
import traceback
from .Base.parser import input_datatset_loader
from .Engine.ipdata_processor import source_processor
from .Base.model import (
    data, Question_stat, path_dict,
    MinimalSearchResults, StudentSearchResults,
)
from .Engine.tokenizer import tokenize, encode, decode, document_sort
from .Engine.retrieval import BM25_retrieval


data = data()


class RagCLI:
    """RAG pipeline commands."""

    def _build(self, max_chunk_size: int):
        tokenized = source_processor(data, max_chunk_size)
        return document_sort(data.documents, tokenized)

    def index(self, max_chunk_size: int = 2000) -> None:
        "Build the index under data/processes/."
        self._build(max_chunk_size)

        # writing an output with the vocab dict
        os.makedirs("data/processed", exist_ok=True)
        with open("data/processed/index_file.json", "w",
                  encoding="utf-8") as f:
            # json.dump(vocab_dict, f, indent=4)
            json.dump(data.index_list, f, indent=4)
        print("Ingestion complete! Indices saved under 'data/processed/'")

    def search_dataset(
        self,
        dataset_path: str,
        k: int = 10,
        save_directory: str = path_dict("OUTPUT_PATH"),
        max_chunk_size: int = 2000,
    ) -> None:
        """Search a whole dataset and write a StudentSearchResults JSON."""
        if k <= 0:
            print("Error: k must be greater than 0")
            return
        documents = self._build(max_chunk_size)
        questions = input_datatset_loader(
            dataset_path, Question_stat()).rag_questions
        bm25 = BM25_retrieval(data, documents, questions)

        results = []
        for q, scored in zip(questions, bm25.query_score):
            results.append(MinimalSearchResults(
                question_id=q.question_id,
                question=q.question,
                retrieved_sources=[n.source for _, n in scored[:k]],
            ))
        out = StudentSearchResults(search_results=results, k=k)

        os.makedirs(save_directory, exist_ok=True)
        out_path = os.path.join(save_directory,
                                os.path.basename(dataset_path))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out.model_dump_json(indent=2))
        print(f"Saved student_search_results to {out_path}")


    # def search(self, query:str=, k: int = 10) -> None:
    #     """Print the top-k sources for one query."""
    #     question_stat = Question_stat()
    #     answer_stat = Question_stat()

    #     question_nodes = input_datatset_loader(args.dataset_path, question_stat).rag_questions
    #     print(question_stat.stat)
    #     given_answer_nodes = answer_loader(args.answer_path, answer_stat).rag_questions
    #     print(answer_stat.stat)

if __name__ == "__main__":
    try:
        fire.Fire(RagCLI)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


    # print(encode(data, tokenize(data, "tokenization")))
    # print(decode(data, encode(data, tokenize(data, "tokenization"))))