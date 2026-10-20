#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   md_text_chunking.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/17 10:11:42 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/20 13:05:12 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


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
            end_index - start_index + 1,
            start_index,
            end_index))


def split(
    markdown_list, code_lines,
    file_path, max_char,
    start_index, actual_end_index
):
    """Given a big chunk inside the markdown files,
    this function breaks it into smaller chunks"""
    overlap: int = 100

    while code_lines != "":

        lines = code_lines[:max_char]
        code_lines = code_lines[(max_char - overlap):]
        end_index = start_index + max_char
        markdown_list.append(
                    push(lines, file_path, start_index, end_index))
        start_index += (max_char - overlap)
    return markdown_list


def md_processor(
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a markdown file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""
    code_lines: str = ""
    end: int
    start_index: int = 0
    end_index: int = 0
    markdown_list: list[MarkdownChunk] = []

    with open(file_path, 'r', encoding='utf-8') as file_object:

        content = file_object.read()
        buffer = content
        while buffer != "":
            if "\n\n---\n\n" in buffer:
                end = buffer.index('\n\n---\n\n') + len('\n\n---\n\n')
            else:
                end = len(buffer)
            code_lines = buffer[:end]
            end_index = start_index + end - 1
            if (end_index - start_index + 1) <= max_char:
                markdown_list.append(
                    push(
                        code_lines, file_path,
                        start_index, end_index
                    ))
            else:
                split(
                    markdown_list, code_lines,
                    file_path, max_char, start_index, end_index)
            start_index += end
            buffer = buffer[end:]

        for obj in markdown_list:
            print(f"[{obj.text}]: {obj.start_index}, {obj.end_index} \n\n")




        # for line in content.splitlines():

        #     if left_over != "":
        #         code_lines = left_over
        #         start_index = start_index - len(left_over)
        #     elif "---" in line:
        #         breaking_point = line.index('---')
        #         code_lines = line[:breaking_point]
        #         left_over = line[breaking_point:]
        #         buffer = ""
        #     else:
        #         code_lines = line[:max_char]
        #         buffer = line[(max_char - overlap):]

        #     print(".")
        #     while buffer != "" or markdown_list == []:
        #         end_index = start_index + len(code_lines)
        #         markdown_list.append(
        #             push(code_lines, file_path, start_index, end_index))
        #         start_index = end_index - overlap
        #         code_lines = buffer[:max_char]
        #         buffer = buffer[(max_char - overlap):]

        #         if buffer == "" and code_lines != "":
        #             end_index = start_index + len(code_lines)
        #             markdown_list.append(
        #                 push(code_lines, file_path, start_index, end_index))

























        # for line in content.splitlines():

        #     if left_over != "":
        #         code_lines = left_over
        #         start_index = start_index - len(left_over)
        #     elif "---" in line:
        #         breaking_point = line.index('---')
        #         code_lines = line[:breaking_point]
        #         left_over = line[breaking_point:]
        #         buffer = ""
        #     else:
        #         code_lines = line[:max_char]
        #         buffer = line[(max_char - overlap):]

        #     print(".")
        #     while buffer != "" or markdown_list == []:
        #         end_index = start_index + len(code_lines)
        #         markdown_list.append(
        #             push(code_lines, file_path, start_index, end_index))
        #         start_index = end_index - overlap
        #         code_lines = buffer[:max_char]
        #         buffer = buffer[(max_char - overlap):]

        #         if buffer == "" and code_lines != "":
        #             end_index = start_index + len(code_lines)
        #             markdown_list.append(
        #                 push(code_lines, file_path, start_index, end_index))

        # for obj in markdown_list:
        #     print(f"{obj.text}: {obj.start_index}, {obj.end_index}")
        #     print(f"{obj.file_path}")


    #    for line in content.splitlines():

    #         if left_over != "":
    #             code_lines = left_over
    #             start_index = start_index - len(left_over)
    #         elif "---" in line:
    #             breaking_point = line.index('---')
    #             code_lines = line[:breaking_point]
    #             left_over = line[breaking_point:]
    #             buffer = ""
    #         else:
    #             code_lines = line[:max_char]
    #             buffer = line[(max_char - overlap):]

    #         print(".")
    #         while buffer != "" or markdown_list == []:
    #             end_index = start_index + len(code_lines)
    #             markdown_list.append(
    #                 push(code_lines, file_path, start_index, end_index))
    #             start_index = end_index - overlap
    #             code_lines = buffer[:max_char]
    #             buffer = buffer[(max_char - overlap):]

    #             if buffer == "" and code_lines != "":
    #                 end_index = start_index + len(code_lines)
    #                 markdown_list.append(
    #                     push(code_lines, file_path, start_index, end_index))













            # if (line.strip().startswith("#") and code_block == []):
            #     code_lines = line[:max_char]

            # elif (line.strip().startswith("#") and code_block != []):
            #     code_block = "\n".join(code_lines)
            #     code_lines = line[:max_char]

            # else:
            #     code_lines = line[:max_char]






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

