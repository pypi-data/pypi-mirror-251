import random


def make_if_statement(processing):
    feature_list = ['A', 'B', 'C']
    select_feature1 = random.choice(feature_list)
    if_figure = random.randint(0, 20)
    processing += f'if row["{select_feature1}"] < {if_figure}:\n'
    constant = random.randint(0, 30)
    processing += f'    y = {constant}\n'
    return processing


def make_elif_statement(processing):
    feature_list = ['A', 'B', 'C']
    select_feature1 = random.choice(feature_list)
    if_figure = random.randint(0, 20)
    processing += f'elif row["{select_feature1}"] < {if_figure}:\n'
    constant = random.randint(0, 30)
    processing += f'    y = {constant}\n'
    return processing


def make_else_statement(processing):
    processing += 'else:\n'
    constant = random.randint(0, 10)
    processing += f'    y = {constant}\n'
    return processing


def branch_easy_model():
    processing = ''

    # if文の数
    num_if = random.randint(1, 3)

    if num_if == 1:
        processing = make_if_statement(processing)
        processing = make_else_statement(processing)
        return processing

    elif num_if == 2:
        processing = make_if_statement(processing)
        processing = make_elif_statement(processing)
        processing = make_else_statement(processing)
        return processing

    elif num_if == 3:
        processing = make_if_statement(processing)
        processing = make_elif_statement(processing)
        processing = make_elif_statement(processing)
        processing = make_else_statement(processing)
        return processing
