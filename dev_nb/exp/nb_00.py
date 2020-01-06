
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/00_nn.ipynb

from fastcore.all import *
from torch import nn, optim, tensor, Tensor
from torch.utils.data import TensorDataset, Dataset, DataLoader

data_path=Path(r'd:\git\dl\data')
mnist_path=data_path.joinpath('mnist.pkl.gz')
Path.ls=lambda x: L(x.iterdir())

Rank0Tensor = NewType('OneEltTensor', Tensor)
LossFunction = Callable[[Tensor, Tensor], Rank0Tensor]
Model = nn.Module

def is_listy(x:Any)->bool: return isinstance(x, (tuple,list))

def loss_batch(model:Model, xb:Tensor, yb:Tensor,
               loss_fn:LossFunction, opt:optim.Optimizer=None):
    "Calculate loss for the batch `xb,yb` and backprop with `opt`"
    if not is_listy(xb): xb = [xb]
    if not is_listy(yb): yb = [yb]
    loss = loss_fn(model(*xb), *yb)

    if opt is not None:
        loss.backward()
        opt.step()
        opt.zero_grad()

    return loss.item(), len(yb)

def fit(epochs:int, model:Model, loss_fn:LossFunction,
        opt:optim.Optimizer, train_dl:DataLoader, valid_dl:DataLoader):
    "Train `model` on `train_dl` with `optim` then validate against `valid_dl`"
    for epoch in range(epochs):
        model.train()
        for xb,yb in train_dl: loss,_ = loss_batch(model, xb, yb, loss_fn, opt)

        model.eval()
        with torch.no_grad():
            losses,nums = zip(*[loss_batch(model, xb, yb, loss_fn)
                                for xb,yb in valid_dl])
        val_loss = np.sum(np.multiply(losses,nums)) / np.sum(nums)

        print(epoch, val_loss)

LambdaFunc = Callable[[Tensor],Tensor]
class Lambda(nn.Module):
    "An easy way to create a pytorch layer for a simple `func`"
    def __init__(self, func:LambdaFunc):
        "create a layer that simply calls `func` with `x`"
        super().__init__()
        self.func=func

    def forward(self, x): return self.func(x)

def noop(x): return x

def ResizeBatch(*size:int) -> Tensor:
    "Layer that resizes x to `size`, good for connecting mismatched layers"
    return Lambda(lambda x: x.view((-1,)+size))
def Flatten()->Tensor:
    "Flattens `x` to a single dimension, often used at the end of a model"
    return Lambda(lambda x: x.view((x.size(0), -1)))
def PoolFlatten()->nn.Sequential:
    "Apply `nn.AdaptiveAvgPool2d` to `x` and then flatten the result"
    return nn.Sequential(nn.AdaptiveAvgPool2d(1), Flatten())

def conv2d(ni:int, nf:int, ks:int=3, stride:int=1, padding:int=None, bias=False) -> nn.Conv2d:
    "Create `nn.Conv2d` layer: `ni` inputs, `nf` outputs, `ks` kernel size. `padding` defaults to `k//2`"
    if padding is None: padding = ks//2
    return nn.Conv2d(ni, nf, kernel_size=ks, stride=stride, padding=padding, bias=bias)

def conv2d_relu(ni:int, nf:int, ks:int=3, stride:int=1,
                padding:int=None, bn:bool=False) -> nn.Sequential:
    "Create a `conv2d` layer with `nn.ReLU` activation and optional(`bn`) `nn.BatchNorm2d`"
    layers = [conv2d(ni, nf, ks=ks, stride=stride, padding=padding), nn.ReLU()]
    if bn: layers.append(nn.BatchNorm2d(nf))
    return nn.Sequential(*layers)

def conv2d_trans(ni:int, nf:int, ks:int=2, stride:int=2, padding:int=0) -> nn.ConvTranspose2d:
    "Create `nn.nn.ConvTranspose2d` layer: `ni` inputs, `nf` outputs, `ks` kernel size. `padding` defaults to 0"
    return nn.ConvTranspose2d(ni, nf, kernel_size=ks, stride=stride, padding=padding)

@dataclass
class DatasetTfm(Dataset):
    "Applies `tfm` to `ds`"
    ds: Dataset
    tfm: Callable = None

    def __len__(self): return len(self.ds)

    def __getitem__(self,idx:int):
        "Apply `tfm` to `x` and return `(x[idx],y[idx])`"
        x,y = self.ds[idx]
        if self.tfm is not None: x = self.tfm(x)
        return x,y

def simple_cnn(actns:Collection[int], kernel_szs:Collection[int],
               strides:Collection[int]) -> nn.Sequential:
    "CNN with `conv2d_relu` layers defined by `actns`, `kernel_szs` and `strides`"
    layers = [conv2d_relu(actns[i], actns[i+1], kernel_szs[i], stride=strides[i])
        for i in range(len(strides))]
    layers.append(PoolFlatten())
    return nn.Sequential(*layers)

def ifnone(a:bool,b:Any):
    "`a` if its not None, otherwise `b`"
    return b if a is None else a

default_device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
Tensors = Union[Tensor, Collection['Tensors']]

def to_device(b:Tensors, device:torch.device):
    "Ensure `b` is on `device`"
    device = ifnone(device, default_device)
    if is_listy(b): return [to_device(o, device) for o in b]
    return b.to(device)

@dataclass
class DeviceDataLoader():
    "`DataLoader` that ensures batches from `dl` are on `device`"
    dl: DataLoader
    device: torch.device

    def __len__(self) -> int: return len(self.dl)
    def proc_batch(self,b:Tensors): return to_device(b, self.device)

    def __iter__(self)->Tensors:
        "Ensure batches from `dl` are on `device` as we iterate"
        self.gen = map(self.proc_batch, self.dl)
        return iter(self.gen)

    @classmethod
    def create(cls, *args, device:torch.device=default_device, **kwargs): return cls(DataLoader(*args, **kwargs), device=device)

TItem = TypeVar('TItem')
TfmCallable = Callable[[TItem],TItem]
TfmList = Union[TfmCallable, Collection[TfmCallable]]
Tfms = Optional[TfmList]

@dataclass
class DataBunch():
    "Bind `train_dl`, `valid_dl` to `device`"
    train_dl:DataLoader
    valid_dl:DataLoader
    device:torch.device=None

    @classmethod
    def create(cls, train_ds:Dataset, valid_ds:Dataset, bs:int=64,
               train_tfm:Tfms=None, valid_tfm:Tfms=None, device:torch.device=None, **kwargs):
        return cls(DeviceDataLoader.create(DatasetTfm(train_ds, train_tfm), bs,   shuffle=True,  device=device, **kwargs),
                   DeviceDataLoader.create(DatasetTfm(valid_ds, valid_tfm), bs*2, shuffle=False, device=device, **kwargs),
                   device=device)

class Learner():
    "Train `model` on `data` for `epochs` using learning rate `lr` and `opt_fn` to optimize training"
    def __init__(self, data:DataBunch, model:Model):
        self.data,self.model = data,to_device(model, data.device)

    def fit(self, epochs, lr, opt_fn=optim.SGD):
        opt = opt_fn(self.model.parameters(), lr=lr)
        loss_fn = F.cross_entropy
        fit(epochs, self.model, loss_fn, opt, self.data.train_dl, self.data.valid_dl)