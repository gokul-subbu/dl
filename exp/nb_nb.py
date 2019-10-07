
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/nb_01.ipynb

import operator

def test(a, b, cmp, cname=None):
    if cname==None: cname==cmp.__name__
    assert cmp(a,b),f'{cname}:\n{a}\n{b}'

def test_eq(a, b):
    test(a, b, operator.eq)

import matplotlib.pyplot as plt
import gzip, math, torch, pickle, matplotlib as mpl
from IPython.core.debugger import set_trace
from torch import tensor
from pathlib import Path
from torch.nn import init

mnist_path=Path(r'D:\git\dl\data\mnist.pkl.gz')

def normalize(x, m, s): return (x-m)/s

def test_near_zero(a,tol=1e-3): assert a.abs()<tol, f"Near zero: {a}"

def mse(output, targ): return (output.squeeze(-1) - targ).pow(2).mean()

import torch.nn.functional as F

def accuracy(out, yb): return (torch.argmax(out, dim=1)==yb).float().mean()

class Dataset():
    def __init__(self, x, y):
        self.x, self.y= x, y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i], self.y[i]

def get_dls(train_ds, valid_ds, bs, **kwargs):
    return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, batch_size=bs*2, **kwargs))