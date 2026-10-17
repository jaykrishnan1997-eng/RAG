#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   md_text_chunking.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/17 10:11:42 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/17 13:26:47 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import re
from dataclasses import dataclass, field

        
@dataclass
class MarkdownChunk:
    text: str
    heading_path: list
    char_count: int = 0


def md_txt_file_processor(
    file_path: str, last_character_index: int,
    max_char: int,
) -> list[int, int]:
    """Given a markdown file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""
    buffer: list[str] = []

    def headings():
        
    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()
        for line in content.splitlines():

            # Heading
            if (line.trim().startswith("#") and code_block == []):
                code_lines.append(line)
            elif (line.trim().startswith("'''") and code_block != []):
                code_block = "\n".join(code_lines)
                code_lines.append(line)
            else:
                code_line.append(line)
            if (sum(len(block) for block in buffer) + len(code_block)) > max_char:
                push()
            
















# def md_txt_chunking(
#     text: str, max_tokens: int, model_name='all-MiniLM-L6-v2'
# ):
#     """AST based recursive split and merge chunking statergy
#      specific to python files"""
#     chunks = []
#     current_chunk = []
#     md_seperators = [
#         "\n##",     # H2 headers (major sections)
#         "\n###",    # H3 headers (subsections)
#         "\n####",   # H4 headers
#         "\n\n",     # Paragraphs
#         "\n",       # Lines
#         ". ",       # Sentences
#         " ",        # Words
#         ""          # Characters
#     ]
#     txt_seperators = [
#         "\n\n",     # Blank lines(logical blocks)
#         "\n",       # Lines
#         ". ",       # Words
#         " ",        # Words
#         ""          # Characters
#     ]
#     current_tok_len = 0
#     current_embedding = None

#     model = SentenceTransformer(model_name)
#     sentences = nltk.sent_tokenize(text)
#     embeddings = model.encode(sentences, convert_to_tensor=True)

#     for i, sentence in enumerate(sentences):
#         sentence_tok_len = len(sentence.split())
#         if current_tok_len + sentence_tok_len <= max_tokens:
#             current_tok_len += sentence_tok_len
#             current_chunk.append(sentence)
#             if current_embedding is None:
#                 current_embedding = embeddings[i]
#             else:
#                 current_embedding = util.pytorch_cos_sim(
#                     current_embedding, embeddings[i]).mean()
#         else:
#             chunks.append(' '.join(current_chunk))
#             current_chunk = [sentence]
#             current_tok_len = sentence_tok_len
#             current_embedding = embeddings[i]
#     if current_chunk:
#         chunks.append(' '.join(current_chunk))
#     return chunks
