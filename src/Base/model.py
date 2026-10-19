#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   model.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/10 13:20:17 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/19 09:40:58 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import uuid
from pydantic import BaseModel, Field
from typing import List


def path_dict(path_abbr: str) -> str:
    path = {
        # "DATA_PATH": "data/raw/vllm-0.10.1",
        "DATA_PATH": "test/test.md",
        "ip_ans_code_path":
        "data/datasets/AnsweredQuestions/dataset_code_public.json",
        "ip_ans_docs_path":
        "data/datasets/AnsweredQuestions/dataset_docs_public.json",
        "ip_unans_code_path":
        "data/datasets/UnansweredQuestions/dataset_code_public.json",
        "ip_unans_docs_path":
        "data/datasets/UnansweredQuestions/dataset_docs_public.json",
        "STUDENT_SEARCH_RESULTS_PATH":
        ("data/output/search_results/UnansweredQuestions"
            "/dataset_docs_public.json"),
        "OUTPUT_PATH": "data/output/search_results/UnansweredQuestions",
        "VECTOR_PATH": "data/vector"
    }
    return path[path_abbr]


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    question_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int
