import random


def make_if_statement(processing):
    feature_list = ['A', 'B', 'C']
    select_feature1 = random.choice(feature_list)
    if_figure = random.randint(0, 20)
    processing += f'if row["{select_feature1}"] < {if_figure}:\n'
    coef_A = random.randint(0, 10)
    coef_B = random.randint(0, 10)
    coef_C = random.randint(0, 10)
    processing += f'    y = {coef_A}*row["A"] + {coef_B}*row["B"] + {coef_C}*row["C"]\n'
    return processing


def make_elif_statement(processing):
    feature_list = ['A', 'B', 'C']
    select_feature1 = random.choice(feature_list)
    if_figure = random.randint(0, 20)
    processing += f'elif row["{select_feature1}"] < {if_figure}:\n'
    coef_A = random.randint(0, 10)
    coef_B = random.randint(0, 10)
    coef_C = random.randint(0, 10)
    processing += f'    y = {coef_A}*row["A"] + {coef_B}*row["B"] + {coef_C}*row["C"]\n'
    return processing


def make_else_statement(processing):
    processing += 'else:\n'
    coef_A = random.randint(0, 10)
    coef_B = random.randint(0, 10)
    coef_C = random.randint(0, 10)
    processing += f'    y = {coef_A}*row["A"] + {coef_B}*row["B"] + {coef_C}*row["C"]\n'
    return processing


def branchlinear_model():
    processing = ''

    # if文の数
    num_if = random.randint(0, 2)

    if num_if == 0:
        coef_A = random.randint(0, 10)
        coef_B = random.randint(0, 10)
        coef_C = random.randint(0, 10)
        processing += f'y = {coef_A}*row["A"] + {coef_B}*row["B"] + {coef_C}*row["C"]'
        return processing

    elif num_if == 1:
        # if文の条件にする特徴量
        processing = make_if_statement(processing)
        processing = make_else_statement(processing)
        return processing

    elif num_if == 2:
        # if文の条件にする特徴量
        processing = make_if_statement(processing)
        processing = make_elif_statement(processing)
        processing = make_else_statement(processing)
        return processing

