#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   recall.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/10 13:44:49 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/20 12:06:38 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


# class Recall_at_k:
#     def __init__(self, documents, bm25, ):
# def recall(self, bm25, expected, k):
#     success = 0
#     for q, (path, s, e) in enumerate(expected):
#         for score, node in bm25.query_score[q][:k]:
#             src = node.source
#             if (
#                 src.file_path.endswith(path)
#                 and src.first_character_index <= e
#                 and src.last_character_index >= s
#             ):
#                 success += 1
#                 break
#     return success / len(expected)

# for k in (1, 5, 10):
#     print(k, Recall_at_k.recall(bm25, expected, k))

def iou(result_unit, ground_truth_unit):
    s1 = result_unit.first_character_index
    s2 = ground_truth_unit.first_character_index
    e1 = result_unit.last_character_index
    e2 = ground_truth_unit.last_character_index

    overlap = max(0, min(e1, e2) - max(s1, s2) + 1)
    union = (e1 - s1 + 1) + (e2 - s2 + 1) - overlap
    if union != 0:
        return (overlap / union)
    else:
        return (0)


def recall(result, ground_truth, k):
    success = 0
    for q, (path, s, e) in enumerate(ground_truth):
        for score, node in bm2.query_score[q][:k]:
            src = node.source
            if (
                src.file_path.endswith(path)
                and src.first_character_index <= e
                and src.last_character_index >= s
            ):
                success += 1
                break
    return success / len(ground_truth)

for k in (1, 5, 10):
    print(k, Recall_at_k.recall(bm25, expected, k))

# Load the student results (StudentSearchResults) and the ground-truth file (via answer_loader, so you get the sources per question).
# For each question, match by question_id.
# For each correct source, check whether any of your top-k results is in the same file and has IoU >= 0.05 with its range.
# Recall for that question = found sources / total sources. Average over questions.
# Print recall@1, 3, 5, 10, matching the moulinette’s format.

# IoU for two ranges on one file: overlap = max(0, min(e1, e2) - max(s1, s2) + 1),
# union = (e1 - s1 + 1) + (e2 - s2 + 1) - overlap, IoU = overlap / union.

# Handle missing files and malformed JSON with a message, like your other commands. A nice side effect: you can compare its numbers with the moulinette’s (0.83 and 0.606), which confirms your IoU logic is right.
