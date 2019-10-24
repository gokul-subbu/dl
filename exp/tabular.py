import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def desc_null(df): return df.isnull().mean()

def impute_na(df, col, imp_var): return df[col].fillna(imp_var)

def desc_col(df, col): return df[col].mean(), df[col].var()

def plot_cols(df, *cols):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    for i in cols:
        df[i].plot(kind='kde',ax=ax)
    lines, labels=ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')

 
def col_trans(df, feat_mean, feat_median):
    mean_imputer=Pipeline(steps=[('imputer',SimpleImputer(strategy='mean'))])
    median_imputer=Pipeline(steps=[('imputer',SimpleImputer(strategy='median'))])
    preprocessor=ColumnTransformer(transformers=[('mean_imputer',mean_imputer, feat_mean),
                                                 ('median_imputer',median_imputer, feat_median)],
                                   remainder='passthrough')
    return preprocessor

def calculate_top_categories(df, col, how_many=10):
    return [
        x for x in df[col].value_counts().sort_values(ascending=False).head(how_many).index]


def one_hot_encode(train, test, col, top_x_labels):
    for label in top_x_labels:
        train[col+'_'+label]=np.where(
            train['Neighbourhood']==label, 1, 0)
        test[col+'_'+label]=np.where(test['Neighbourhood']==label, 1, 0)


