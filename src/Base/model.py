#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   model.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/10 13:20:17 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 09:19:40 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import uuid
from pydantic import BaseModel, Field
from typing import List


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


class Path_dict():
    Path = {
        "ip_ans_code_path":
        "data/datasets/AnsweredQuestions/dataset_code_public.json",
        "ip_ans_docs_path":
        "data/datasets/AnsweredQuestions/dataset_docs_public.json",
        "ip_unans_code_path":
        "data/datasets/UnansweredQuestions/dataset_code_public.json",
        "ip_unans_docs_path":
        "data/datasets/UnansweredQuestions/dataset_docs_public.json",
        "student_search_results_path":
        " data/output/search_results/UnansweredQuestions/dataset_docs_public.json",
        "op_path": "data/output/search_results/UnansweredQuestions",
        "processed_path": "data/datasets/processed",
        "vector_path": "data/datasets/vector"
    }
