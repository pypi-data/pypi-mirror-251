import random


def linear_model():
    processing = ''

    coef_A = random.randint(0, 10)
    coef_B = random.randint(0, 10)
    coef_C = random.randint(0, 10)
    processing += f'y = {coef_A}*row["A"] + {coef_B}*row["B"] + {coef_C}*row["C"]'

    return processing
