import pandas as pd
import numpy as np
from ..utils.utils import jinja_rendering

def pseudo_data(num_rows):

    df = pd.DataFrame({
        'A': np.random.randint(0, 21, size=num_rows),
        'B': np.random.randint(0, 21, size=num_rows),
        'C': np.random.randint(0, 21, size=num_rows)
    })
    return df

def df_to_string(processing, num_rows):
    code_model = jinja_rendering(processing)
    df = pseudo_data(num_rows)
    local_vars = {}
    exec(code_model, globals(), local_vars)
    df['y'] = local_vars['predict'](df)
    str_df = df.to_string(index=False)
    return str_df
