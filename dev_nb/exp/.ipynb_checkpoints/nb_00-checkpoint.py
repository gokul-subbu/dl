
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/00_test.ipynb


import operator, itertools
from functools import partial
from collections import deque
from numpy import array, ndarray
import pandas as pd

from typing import Any, Collection, Callable, NewType, List, Union, TypeVar, Optional, Generator, Iterable
from pandas.api.types import is_categorical_dtype,is_numeric_dtype
from numpy import array,ndarray
from scipy import ndimage
from IPython.core.debugger import set_trace

try:
    from types import WrapperDescriptorType,MethodWrapperType,MethodDescriptorType
except ImportError:
    WrapperDescriptorType = type(object.__init__)
    MethodWrapperType = type(object().__str__)
    MethodDescriptorType = type(str.join)
from types import BuiltinFunctionType,BuiltinMethodType,MethodType,FunctionType

pd.options.display.max_colwidth = 600
NoneType = type(None)
string_classes = (str,bytes)



def test(a, b, cmp, cname=None):
    'assert cmp(a,b)'
    if cname is None: cname=cmp.__name__
    assert cmp(a, b), f'{cname}: \na\nb'


test_eq= partial(test,cmp=operator.eq, cname='==')
test_ne= partial(test,cmp=operator.ne)


def test_type_eq(a, b):
    test_eq(a,b)
    test_eq(type(a), type(b))
    if isinstance(a, (list, tuple)): test_eq(map(type, a), map(type, b))

def test_shuffled(a,b):
    "`test` that `a` and `b` are shuffled versions of the same sequence of items"
    test_ne(a, b)
    test_eq(Counter(a), Counter(b))

def test_close(a,b,eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a,b,partial(is_close,eps=eps),'close')

def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')

def test_stdout(f, exp, regex=False):
    "Test that `f` prints `exp` to stdout, optionally checking as `regex`"
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')

def test_warns(f, show=False):
    with warnings.catch_warnings(record=True) as w:
        f()
        test_ne(len(w), 0)
        if show:
            for e in w: print(f"{e.category}: {e.message}")

def test_fig_exists(ax):
    "Test there is a figure displayed in `ax`"
    assert ax and len(np.frombuffer(ax.figure.canvas.tostring_argb(), dtype=np.uint8))
    
def is_iter(o):
    "Test whether `o` can be used in a `for` loop"
    #Rank 0 tensors in PyTorch are not really iterable
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

def is_coll(o):
    "Test whether `o` is a collection (i.e. has a usable `len`)"
    #Rank 0 tensors in PyTorch do not have working `len`
    return hasattr(o, '__len__') and getattr(o,'ndim',1)

def all_equal(a,b):
    "Compares whether `a` and `b` are the same length and have the same contents"
    if not is_iter(b): return False
    return all(equals(a_,b_) for a_,b_ in itertools.zip_longest(a,b))

def noop (x=None, *args, **kwargs):
    "Do nothing"
    return x

def noops(self, x=None, *args, **kwargs):
    "Do nothing (method)"
    return x

def one_is_instance(a, b, t): return isinstance(a,t) or isinstance(b,t)

def equals(a,b):
    "Compares `a` and `b` for equality; supports sublists, tensors and arrays too"
    if one_is_instance(a,b,type): return a==b
    if hasattr(a, '__array_eq__'): return a.__array_eq__(b)
    if hasattr(b, '__array_eq__'): return b.__array_eq__(a)
    cmp = (np.array_equal if one_is_instance(a, b, ndarray       ) else
           operator.eq    if one_is_instance(a, b, (str,dict,set)) else
           all_equal      if is_iter(a) or is_iter(b) else
           operator.eq)
    return cmp(a,b)