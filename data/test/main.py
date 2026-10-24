import ast

with open('ft_garden_analytics.py', 'r') as f:
    code = f.read()
    code_lines = f.readlines()
tree = ast.parse(code)
# 
# for node in ast.walk(tree):
#     # print(node)
#     # print(node.__dict__)
#     # print("children: " + str([x for x in ast.iter_child_nodes(node)])
#     #     + "\n")
#     print(ast.unparse(node))
# print(ast.dump(tree, indent=4))
# print([node for node in ast.walk(tree)])

# print(ast.dump(tree, indent=4))

# body_value = []
# for name, value in ast.iter_fields(tree):
#     if value != []:
#         body_value.append(value)
#     # print(name, value)
#     # print("\n ----------------------------- \n")
#     # print(ast.unparse(value))
# print(ast.unparse(body_value[0]))

# print("$$$$$$$$$$")
# # for name, value in ast.iter_fields(body_value[0]):
# #     print(name, value)
# print(body_value[0])
# print(tree.body[0])
# print(ast.unparse(tree.body[0]))
# print([tree.body[0].body])
# print("\n\n")
# for obj in [tree.body[0].body]:



# print(tree.body)
# print(tree.body[0].lineno)
# print(tree.body[0].end_lineno)
# print(tree.body[1].lineno)
# print(tree.body[1].end_lineno)




# node_list = tree.body[0].body
# print(node_list)
# print(ast.unparse(node_list[1]))
# print(len(ast.unparse(node_list[1])))
# print(node_list[1].lineno)
# print(node_list[1].end_lineno)



line_dict = {}
content_copy = code
for i, line in enumerate(code_lines):
    content_copy = content_copy[len(line):]
    line_dict[i] = code.index(content_copy)
print(line_dict)










# print(ast.unparse([tree.body[0].body][0]))

# for node in ast.iter_child_nodes(tree):
#     print(node.__dict__)
    # print(ast.unparse(node))
# print(ast.dump(node))
# .
# |____main.py
# |____ft_garden_analytics.py
# |____ft_hello_garden.py
# |____ft_garden_name.py
# |____ft_plot_area.py
# |____ft_harvest_total.py
# |____ft_plant_age.py
# |____ft_water_reminder.py
# |____ft_count_harvest_iterative.py
# |____ft_count_harvest_recursive.py
# |____ft_seed_inventory.py

