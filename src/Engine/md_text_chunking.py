#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   md_text_chunking.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/17 10:11:42 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/19 13:47:41 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import re
from dataclasses import dataclass, field


class MarkdownChunk:
    def __init__(
        self,
        text: str,
        file_path: list,
        char_count: int,
        start_index: int,
        end_index: int,
    ):
        self.text: str = text
        self.file_path: list = file_path
        self.char_count: int = char_count
        self.start_index: int = start_index
        self.end_index: int = end_index


def push(code_line, file_path, start_index, end_index):

    return (
        MarkdownChunk(
            code_line,
            file_path,
            end_index - start_index,
            start_index,
            end_index))


def md_processor(
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a markdown file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""
    buffer: str = ""
    code_lines: str = ""
    code_block: list[str] = []
    start_index: int = 0
    end_index: int
    overlap: int = 10
    markdown_list: list[MarkdownChunk] = []

    with open(file_path, 'r', encoding='utf-8') as file_object:

        content = file_object.read()
        for line in content.splitlines():

            # Heading
            if (line.strip().startswith("#") and code_block == []):
                code_lines = line[:max_char]

            elif (line.strip().startswith("#") and code_block != []):
                code_block = "\n".join(code_lines)
                code_lines = line[:max_char]

            else:
                code_lines = line[:max_char]

            buffer = line[(max_char - overlap):]
            breakpoint()
            while buffer != "" or markdown_list == []:
                end_index = start_index + len(code_lines)
                markdown_list.append(
                    push(code_lines, file_path, start_index, end_index))
                start_index = end_index - overlap
                code_lines = buffer[:max_char]
                buffer = buffer[(max_char - overlap):]

                if buffer == "" and code_lines != "":
                    end_index = start_index + len(code_lines)
                    markdown_list.append(
                        push(code_lines, file_path, start_index, end_index))

            for obj in markdown_list:
                print(f"{obj.text}: {obj.start_index}, {obj.end_index}")
                print(f"{obj.file_path}")



            # # Heading
            # breakpoint()
            # if (line.strip().startswith("#") and code_block == []):
            #     code_lines.append(line)
            # elif (line.strip().startswith("#") and code_block != []):
            #     code_block = "\n".join(code_lines)
            #     code_lines.append(line)
            # else:
            #     code_lines.append(line)
            # end_index = sum(len(block) for block in buffer)
            # if (end_index + len(code_block)) > max_char:
            #     markdown_list.append(
            #         push(buffer, file_path, start_index, end_index))
            #     print(buffer)
            #     buffer = []
            #     start_index = end_index - overlap
            # buffer.append(code_block)
            # code_block = []
















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

