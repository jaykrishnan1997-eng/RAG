#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/17 11:42:09 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import re
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


def _grounded(answer: str, context: str) -> bool:
    words = set(re.findall(r"[a-z0-9_]{4,}", answer.lower()))
    if not words:
        return False
    ctx = context.lower()
    hits = sum(w in ctx for w in words)
    return hits / len(words) >= 0.5


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

    def answer(self, query: str, k: int = 5) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        MIN_SCORE = 12.0
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
        # print("top score:", results[0][0] if results else None) # temporary
        if not results or results[0][0] < MIN_SCORE:
            print("I cannot find the answer in the provided sources.")
            return
        context = ""
        for i, (_, node) in enumerate(results, 1):
            context += (f"[Source {i}: {node.source.file_path}]\n"
                        f"{node.text}\n\n")

        MODEL = "Qwen/Qwen3-0.6B"

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL, torch_dtype="auto")

        messages = [
            {"role": "system", "content": (
                "You answer questions about the vLLM codebase using ONLY the "
                "provided context. Never use outside knowledge. If the context "
                "does not contain the answer, reply exactly: "
                "\"I cannot find the answer in the provided sources.\""
            )},
            {"role": "user", "content": (
                f"Context:\n{context}\n\nQuestion: {query}\n\n"
                "Answer ONLY from the context above."
            )},
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        out = model.generate(**inputs, max_new_tokens=200, do_sample=False)
        answer = tokenizer.decode(
            out[0][inputs.input_ids.size(-1):], skip_special_tokens=True
        ).strip()
        if not _grounded(answer, context):
            answer = "I cannot find the answer in the provided sources."
        print(answer)

    def answer_dataset(
        student_search_results_path: str = path_dict("ip_unans_path"),
        save_directorystr: str = path_dict("OUTPUT_PATH")
    ):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        StudentSearchResults.model_validate_json

        MIN_SCORE = 12.0
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
        # print("top score:", results[0][0] if results else None) # temporary
        if not results or results[0][0] < MIN_SCORE:
            print("I cannot find the answer in the provided sources.")
            return
        context = ""
        for i, (_, node) in enumerate(results, 1):
            context += (f"[Source {i}: {node.source.file_path}]\n"
                        f"{node.text}\n\n")

        MODEL = "Qwen/Qwen3-0.6B"

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL, torch_dtype="auto")

        messages = [
            {"role": "system", "content": (
                "You answer questions about the vLLM codebase using ONLY the "
                "provided context. Never use outside knowledge. If the context "
                "does not contain the answer, reply exactly: "
                "\"I cannot find the answer in the provided sources.\""
            )},
            {"role": "user", "content": (
                f"Context:\n{context}\n\nQuestion: {query}\n\n"
                "Answer ONLY from the context above."
            )},
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        out = model.generate(**inputs, max_new_tokens=200, do_sample=False)
        answer = tokenizer.decode(
            out[0][inputs.input_ids.size(-1):], skip_special_tokens=True
        ).strip()
        if not _grounded(answer, context):
            answer = "I cannot find the answer in the provided sources."
        print(answer)


if __name__ == "__main__":
    try:
        fire.Fire(RagCLI)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
