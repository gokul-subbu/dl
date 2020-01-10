import pandas as pd
import numpy as np

class dframe():
    def __init__(self, df:pd.DataFrame):
        self.df=df
        self.cols=df.shape[0]

    def split_val(self, val_pct:float=0.3):
        idx=np.arange(cols)])
        shuf_idx=np.random.shuffle(idx)
        train_idx, val_idx=shuf_idx[int(val_pct*cols):], shuf_idx[:int(val_pct*cols)]
        return self.df[train_idx], self.df[val_idx]

    
