#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   recall.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/11/10 13:44:49 by jkrishna            #+#    #+#            #
#   Updated: 2026/11/11 18:58:41 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #


class Recall_at_k:
    def __init__(self, documents, ):
    def recall(self, bm25, expected, k):
        success = 0
        for q, (path, s, e) in enumerate(expected):
            for score, node in bm25.query_score[q][:k]:
                src = node.source
                if (
                    src.file_path.endswith(path)
                    and src.first_character_index <= e
                    and src.last_character_index >= s
                ):
                    success += 1
                    break
        return success / len(expected)

    for k in (1, 5, 10):
        print(k, Recall_at_k.recall(bm25, expected, k))
