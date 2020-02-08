
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/02_df.ipynb

from export.nb_01 import *
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_categorical_dtype
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
from typing import Tuple

pd.pandas.set_option('display.max_columns', None)

Path.ls= lambda x: [i.name for i in os.scandir()]

def get_sample(df: pd.DataFrame, n:int)-> pd.DataFrame:
    idxs= sorted(np.random.permutation(len(df))[:n])
    return df.iloc[idxs].copy()

def train_cats(df:pd.DataFrame):
    for col_name, col in df.items():
        if is_string_dtype(col):
            df[col_name]=col.astype('category').cat.as_ordered()

def apply_cats(df:pd.DataFrame, df_train:pd.DataFrame):
    for col_name, col in df.items():
        if (col_name in df_train.columns) and (df_train[col_name].dtype.name=='category'):
            df[col_name]=pd.Categorical(col, categories=df_train[col_name].cat.categories, ordered=True)

def fill_missing(df:pd.DataFrame, col_name: str, na_dict:dict=None):
    na_dict=() if na_dict is None else na_dict
    col=df[col_name]
    if is_numeric_dtype(col) and (pd.isnull(col).sum() or (col_name in na_dict)):
        df[col_name+'_na']=pd.isnull(col)
        filler=na_dict[col_name] if col_name in na_dict else col.median()
        df[col_name]=col.fillna(filler)
        na_dict[col_name]=filler
    return na_dict

def numericalize(df:pd.DataFrame, col_name, max_n_cat=-1, nans_to_zero=True):
    col=df[col_name]
    if not is_numeric_dtype(col) and len(col.cat.categories)> max_n_cat:
        df[col_name]=col.cat.codes
        if nans_to_zero:
            df[col_name]+=1

def proc_df(df:pd.DataFrame, y_fld:str=None,
           na_dict:dict=None, skip_flds:list=None,
           ignore_flds:list=None, max_n_cat: int=-1):
    '''
    returns df, y, na_dict
    '''
    if skip_flds is None: skip_flds=[]
    if ignore_flds is None: ignore_flds=[]
    if na_dict is None: na_dict={}

    assert sum(1 if not (is_categorical_dtype(df[col_name])) or
            is_numeric_dtype(df[col_name]) else 0
              for col_name in df.columns), 'all the columns in the df must be of type numerical or categorical'
    df = df.copy()
    ignored_cols = df.loc[:, ignore_flds]
    df.drop(ignore_flds, axis=1, inplace=True)
    y=None
    if y_fld:
        if not is_numeric_dtype(df[y_fld]):
            df[y_fld]= df[y_fld].cat.codes
        y=df[y_fld].values
        skip_flds.append(y_fld)

    df.drop(skip_flds, axis=1, inplace=True)
    for col_name in df.columns:
        fill_missing(df, col_name, na_dict)
        numericalize(df, col_name, max_n_cat=max_n_cat)

    df = pd.get_dummies(df, dummy_na=True)
    df=pd.concat([ignored_cols, df], axis=1)
    return df, y, na_dict

def add_datepart(df:pd.DataFrame, cols:list=None, time:bool=True,inplace:bool=True)->pd.DataFrame:
    '''parameters:
                df: pd.DataFrame
                cols: datetime cols
                just date: bool specifying whether the object is it just date or date time
                inplace: bool'''
    date_part=['year','month','day','week','dayofweek','weekday','quarter','is_month_start','is_month_end','is_year_end']
    time_part=['hour','minute','second']
    for i in cols:
        if time:
            for j in time_part:
                df[f'{i}_{j}']=getattr(df[i].dt,j)
        for j in date_part:
            df[f'{i}_{j}']=getattr(df[i].dt,j)
    df.drop(columns=cols, inplace=True)
    return

def split_val(df:pd.DataFrame, val_pct:float=0.3):
    'returns `df_train` and `df_valid`'
    shuf_idx=np.random.permutation(len(df))
    train_idx, val_idx=shuf_idx[int(val_pct*len(df)):], shuf_idx[:int(val_pct*len(df))]
    return df.iloc[train_idx,:], df.iloc[val_idx,:]

def split_dep_col(df:pd.DataFrame, y:str):
    'returns `x` and `y`'
    return df.drop(columns=y), df.loc[:, y]

def train_test_split(df:pd.DataFrame, y:str=None, val_pct:float=0.3):
    ''' df 'pandas datadrame object `y` is the dependent column val_pct:=0.3'
    returns `x_train`, `y_train`, `x_valid`, `y_valid`'''
    df_train, df_val= split_val(df.copy(), val_pct)
    if y is None:
        return df_train, df_val
    else: return split_dep_col(df_train, y), split_dep_col(df_train, y)

# from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV