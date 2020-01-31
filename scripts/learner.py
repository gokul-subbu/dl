import torch
from torch import nn, optim
def trainable_params(m):
    return [o for o in m.parameters() if o.requires_grad]

Adam=optim.Adam

class Learner():
    def __init__(self, dls, model, loss_func=None, opt_func=Adam, lr=1e-2, splitter=trainable_params,
                 cb_funcs=None, metrics=None, path=None, model_dir='models',wd=0.3, wd_bn_bias=False,
                 moms=(0.95, 0.85, 0.95)):
        self.training, self.create_mbar, self.logger, self.opt, self.cbs=False, True, print, None, L()
        if loss_func is None:
            loss_func=getattr(dls.train_ds, 'loss_func', None)
            assert loss_func is not None, "could not infer loss function from the data"
        self.loss_func=loss_func
        self.path=path if path is not None else getattr(dls, 'path', Path('.'))
        self.add_cbs(cbf() for cbf in L(defaults.callbacks)+L(cb_funcs))
        self.add_cbs(cbs)
        self.model.to(self.dls.device)
        self.epoch, self.n_epoch, self.loss= 0, 1, tensor(0.)

    @property
    def metrics(self): return self._metrics
    
    @pry

