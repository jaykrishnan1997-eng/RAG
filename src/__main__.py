#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/16 11:47:13 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import fire
import json
import pickle
import traceback
from .Base.parser import input_datatset_loader
from .Engine.ipdata_processor import source_processor
from .Base.model import (
    data, Question_stat, path_dict,
    MinimalSearchResults, StudentSearchResults,
    UnansweredQuestion
)
from .Engine.tokenizer import tokenize, encode, decode, document_sort
from .Engine.retrieval import BM25_retrieval


data = data()


class RagCLI:
    """RAG pipeline commands."""

    def _build(self, max_chunk_size: int):
        tokenized = source_processor(data, max_chunk_size)
        return document_sort(data.documents, tokenized)

    def _load(self):
        path = "data/processed/index.pk1"
        with open(path, "rb") as f:
            saved = pickle.load(f)
        data.index_list = saved["index_list"]
        data.current_index = saved["current_index"]
        return saved["documents"]

    def index(self, max_chunk_size: int = 2000) -> None:
        "Build the index under data/processes/."
        documents = self._build(max_chunk_size)

        # writing an output with the vocab dict
        os.makedirs("data/processed", exist_ok=True)
        with open("data/processed/index_file.json", "w",
                  encoding="utf-8") as f:
            # json.dump(vocab_dict, f, indent=4)
            json.dump(data.index_list, f, indent=4)

        with open("data/processed/index.pk1", "wb") as f:
            pickle.dump({
                "index_list": data.index_list,
                "current_index": data.current_index,
                "documents": documents,
            }, f)
        print("Ingestion complete! Indices saved under 'data/processed/'")

    def search_dataset(
        self,
        dataset_path: str,
        k: int = 10,
        save_directory: str = path_dict("OUTPUT_PATH"),
    ) -> None:
        """Search a whole dataset and write a StudentSearchResults JSON."""
        if k <= 0:
            print("Error: k must be greater than 0")
            return
        try:
            documents = self._load()
        except FileNotFoundError:
            print("Error: no index found, run the index command first")
            return
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

    def search(self, query: str, k: int = 10) -> None:
        """Print the top-k sources for one query."""
        query = str(query).strip()
        if not query:
            print("Error: query must not be empty")
            return
        if k <= 0:
            print("Error: k must be greater than 0")
            return
        try:
            documents = self._load()
        except FileNotFoundError:
            print("Error: no index found, run the index command first")
            return

        questions = [UnansweredQuestion(question=query)]
        bm25 = BM25_retrieval(data, documents, questions)
        results = bm25.query_score[0][:k]
        if not results:
            print("No results found")
            return

        for _, node in results:
            src = node.source
            print(f"{src.file_path} "
                  f"[{src.first_character_index}:{src.last_character_index}]")

        def answer():
            query = str(query).strip()
            if not query:
                print("Error: query must not be empty")
                return
            if k <= 0:
                print("Error: k must be greater than 0")
                return
            try:
                documents = self._load()
            except FileNotFoundError:
                print("Error: no index found, run the index command first")
                return

            questions = [UnansweredQuestion(question=query)]
            bm25 = BM25_retrieval(data, documents, questions)
            results = bm25.query_score[0][:k]
            if not results:
                print("No results found")
                return

            for _, node in results:
                src = node.source
                print(f"{src.file_path} "
                    f"[{src.first_character_index}:{src.last_character_index}]")
        


Load the index and retrieve the top k, same as search.
Build a prompt from the chunk texts (node.text), trimmed so the total context stays under about 2000 characters per chunk and a sensible total.
Load Qwen/Qwen3-0.6B once, apply its chat template, and generate with greedy decoding and a cap on new tokens.
Print the answer.

One Qwen3 detail: it has a “thinking” mode that emits a <think>...</think> block before the answer. Turn it off with enable_thinking=False in apply_chat_template, or strip the block from the output. Otherwise your answers will start with reasoning text.

Want to write answer yourself and paste it for review, or go through the prompt wording first?
if __name__ == "__main__":
    try:
        fire.Fire(RagCLI)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


