import pandas as pd
import numpy as np
import torch
from ..utils.utils import jinja_rendering

def ibl_output(model, tokenizer, input):
    prompt = f"### Instruction: {input}\n\n### Response: "

    # 推論の実行
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100
            )
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    output = output.split("### Response: ")[-1]
    return output

def str_to_df(data_str):
    lines = data_str.split('\n')
    data = [line.split() for line in lines]
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.astype(int)
    return df

def code_model_pred(df, code_model):
    df = df.drop(['y'], axis=1)
    local_vars = {}
    exec(code_model, globals(), local_vars)
    df['y'] = local_vars['predict'](df)
    return df



def ibl_boosting(model, tokenizer, input, num_boost_round):

    code_list = []

    for _ in range(num_boost_round):
        code = ibl_output(model, tokenizer, input)
        print(code)
        code_list.append(code)
        df = str_to_df(input)
        code_model = jinja_rendering(code)
        pred_df = code_model_pred(df, code_model)
        input = pred_df.to_string(index=False)
    return code_list
