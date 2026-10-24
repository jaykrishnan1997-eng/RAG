
import ast

class ChunkNode:
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
        ChunkNode(
            code_line,
            file_path,
            len(code_line),
            start_index,
            end_index))

def line_char_dict(content):
    # dictionary of line_number: character_index
    line_dict = {}
    content_copy = content
    for i, line in enumerate(content):
        content_copy = content_copy[len(line):]
        line_dict[i] = content.index(content_copy)
    return line_dict


def recursive_splitter(tree, temp_list, file_path, max_char, line_char_dict):
    node_list = tree.body
    for node in node_list:
        code_line = ast.unparse(node)
        if len(code_line) <= max_char:
            start_char = 
            temp_list.append(push(file_path, node.lineno, node.end_lineneo))
        else:
            temp_list.append(recursive_splitter(node, temp_list, file_path, max_char))
    return (temp_list)

    # if len()
    # print(node_list)
    # print(ast.unparse(node_list[1]))
    # print(node_list[1].lineno)
    # print(node_list[1].end_lineno)


def python_processor(
    chunk_data_list,
    file_path: str,
    max_char: int,
) -> list[int, int]:
    """Given a python file, seperate them in heirarchy tree
    and then access it for chunking. Input: filepath, Output:
    list of first_character_index and last_character_index."""

    with open(file_path, 'r', encoding='utf-8') as file_object:
        content = file_object.read()

    if len(content) <= max_char:
        chunk_data_list.append(push(file_path, 0, len(content)))
        return (chunk_data_list)

    tree = ast.parse(content)
    chunk_data_list.append(recursive_splitter(tree, [], file_path, max_char))

    line_dict = line_char_dict(content)

    for obj in chunk_data_list:
        print(f"[{obj.text}]: {obj.start_index}, {obj.end_index} \n\n")












# def split(
#     chunk_data_list, code_lines,
#     file_path, max_char,
#     start_index, actual_end_index
# ):
#     """Given a big chunk inside the markdown files,
#     this function breaks it into smaller chunks"""
#     overlap: int = int(0.15 * max_char)

#     while code_lines != "":

#         lines = code_lines[:max_char]
#         code_lines = code_lines[(max_char - overlap):]
#         end_index = start_index + max_char
#         chunk_data_list.append(
#                     push(lines, file_path, start_index, end_index))
#         start_index += (max_char - overlap)
#     return chunk_data_list









# # from sentence_transformers import SentenceTransformer

# # # 1. Load a model that supports both text and images
# # model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")

# # # 2. Encode images from URLs
# # img_embeddings = model.encode([
# #     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
# #     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
# # ])

# # # 3. Encode text queries (one matching + one hard negative per image)
# # text_embeddings = model.encode([
# #     "A green car parked in front of a yellow building",
# #     "A red car driving on a highway",
# #     "A bee on a pink flower",
# #     "A wasp on a wooden table",
# # ])

# # # 4. Compute cross-modal similarities
# # similarities = model.similarity(text_embeddings, img_embeddings)
# # print(similarities)
# # # tensor([[0.5115, 0.1078],
# # #         [0.1999, 0.1108],
# # #         [0.1255, 0.6749],
# # #         [0.1283, 0.2704]])
