#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/24 12:12:04 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import re
import sys
import fire
import json
import pickle

from .Base.parser import input_datatset_loader, answer_loader
from .Engine.ipdata_processor import source_processor
from .Base.model import (
    data, Question_stat, path_dict,
    MinimalSearchResults, StudentSearchResults,
    UnansweredQuestion, MinimalAnswer,
    StudentSearchResultsAndAnswer,
)
from .Engine.recall import recall
from .Engine.tokenizer import document_sort
from .Engine.retrieval import BM25_retrieval
from tqdm import tqdm

CACHE = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), ".hf-cache")

data = data()
REFUSAL = "I cannot find the answer in the provided sources."


def _grounded(answer: str, context: str) -> bool:
    words = set(re.findall(r"[a-z0-9_]{4,}", answer.lower()))
    if not words:
        return False
    ctx = context.lower()
    hits = sum(w in ctx for w in words)
    return hits / len(words) >= 0.5


def _generate(tokenizer, model, context: str, question: str) -> str:
    messages = [
        {"role": "system", "content": (
            "You answer questions about the vLLM codebase using ONLY the "
            "provided context. Never use outside knowledge. If the "
            "context does not contain the answer, reply exactly: "
            f"\"{REFUSAL}\""
        )},
        {"role": "user", "content": (
            f"Context:\n{context}\n\nQuestion: {question}\n\n"
            "Answer ONLY from the context above."
        )},
    ]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
        enable_thinking=False)
    inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=120, do_sample=False)
    reply = tokenizer.decode(
        out[0][inputs.input_ids.size(-1):], skip_special_tokens=True
    ).strip()
    if reply.startswith("I cannot find") or not _grounded(reply, context):
        return REFUSAL
    return reply

# def _validateJSON(file):
#     try:
#         json.loads(file)
#     except ValueError:
#         return False
#     return True


class RagCLI:
    """RAG pipeline commands."""

    def _build(self, max_chunk_size: int):
        tokenized = source_processor(data, max_chunk_size)
        return document_sort(data.documents, tokenized)

    def _load(self):
        path = "data/processed/index.pkl"
        with open(path, "rb") as f:
            saved = pickle.load(f)
        data.index_list = saved["index_list"]
        data.current_index = saved["current_index"]
        return saved["documents"]

    def index(self, max_chunk_size: int = 2000) -> None:
        "Build the index under data/processed/."
        documents = self._build(max_chunk_size)

        # writing an output with the vocab dict
        os.makedirs("data/processed", exist_ok=True)
        with open("data/processed/index_file.json", "w",
                  encoding="utf-8") as f:
            # json.dump(vocab_dict, f, indent=4)
            json.dump(data.index_list, f, indent=4)

        with open("data/processed/index.pkl", "wb") as f:
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

        try:
            questions = input_datatset_loader(
                dataset_path, Question_stat()).rag_questions
            if not questions:
                print("Error: no question loaded, nothing to search")
                return
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"Error: cannot load dataset: {e}")
            return
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
        # MIN_SCORE = 12.0
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
        # if not results or results[0][0] < MIN_SCORE:
        #     print("I cannot find the answer in the provided sources.")
        if not results:
            print("No results found")
            return
        context = ""
        for i, (_, node) in enumerate(results, 1):
            context += (f"[Source {i}: {node.source.file_path}]\n"
                        f"{node.text}\n\n")

        MODEL = "Qwen/Qwen3-0.6B"
        context = context[:4000]
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL, cache_dir=CACHE)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL, dtype="float32", cache_dir=CACHE)
        except OSError as e:
            print(f"Error: cannot load {MODEL} (disk space or network?): {e}")
            return

        reply = _generate(tokenizer, model, context, query)
        print(reply)

    def answer_dataset(
        self,
        student_search_results_path: str,
        save_directory: str = path_dict("OUTPUT_PATH"),
    ):
        """Generate answers for a StudentSearchResults JSON."""
        try:
            with open(student_search_results_path, encoding="utf-8") as f:
                search = StudentSearchResults.model_validate_json(f.read())
        except FileNotFoundError:
            print(f"Error: {student_search_results_path} not found")
            return
        except ValueError as e:
            print(f"Error: invalid search results file: {e}")
            return

        from transformers import AutoModelForCausalLM, AutoTokenizer

        MODEL = "Qwen/Qwen3-0.6B"
        # import torch
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL, cache_dir=CACHE)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL, dtype="float32", cache_dir=CACHE)
        except OSError as e:
            print(f"Error: cannot load {MODEL} (disk space or network?): {e}")
            return

        cache: dict[str, str] = {}
        answers = []

        # import torch
        # print(torch.get_num_threads())
        # torch.set_num_threads(os.cpu_count() or 1)
        # print(torch.get_num_threads())
        for item in tqdm(search.search_results, desc="Answering"):
            context = ""
            for i, src in enumerate(item.retrieved_sources, 1):
                if src.file_path not in cache:
                    try:
                        with open(src.file_path, encoding="utf-8") as f:
                            cache[src.file_path] = f.read()
                    except OSError:
                        cache[src.file_path] = ""
                text = cache[src.file_path][
                    src.first_character_index:src.last_character_index + 1]
                context += f"[Source {i}: {src.file_path}]\n{text}\n\n"

            context = context[:4000]

            reply = _generate(tokenizer, model, context, item.question)
            answers.append(MinimalAnswer(
                question_id=item.question_id,
                question=item.question,
                retrieved_sources=item.retrieved_sources,
                answer=reply,
            ))

        out = StudentSearchResultsAndAnswer(
            search_results=answers, k=search.k)
        os.makedirs(save_directory, exist_ok=True)
        out_path = os.path.join(
            save_directory,
            os.path.basename(student_search_results_path))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out.model_dump_json(indent=2))
        print(f"Saved student_search_results_and_answer to {out_path}")

    def evaluate(
        self,
        student_search_results_path: str,
        dataset_path: str,
    ):
        try:
            with open(student_search_results_path, encoding="utf-8") as j:
                result = StudentSearchResults.model_validate_json(j.read())
        except FileNotFoundError as e:
            print(f"Error: file not found: {e}")
            return
        except ValueError as e:
            print(f"Error: invalid search results file: {e}")
            return

        try:
            truth_questions = answer_loader(
                dataset_path, Question_stat()).rag_questions
            if not truth_questions:
                print("Errr: no ground truth questions loaded")
                return

        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"Error: cannot load ground truth: {e}")
            return

        results = {r.question_id: r.retrieved_sources
                   for r in result.search_results}
        truth = {q.question_id: q.sources for q in truth_questions}
        for k in (1, 3, 5, 10):
            print(f"Recall@{k}: {recall(results, truth, k):.3f}")


if __name__ == "__main__":
    try:
        fire.Fire(RagCLI)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
