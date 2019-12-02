# PyTorch Template
A general code template for deep learning experiment in PyTorch.

- __common.py__  
  Define hyperparameters and expriment configuration, which can later be changed by specifying command-line arguments. This config will be used by other modules. Default value for some args like `data_root`, `proj_dir` must be specified.
- __dataset.py__  
  Define customized dataset/dataloader.
- __network.py__  
  Define customized network architecture.
- __agent.py__  
  A base trainer is defined for the control of training process, e.g. forward, backward, loss recording, checkpoint saving/loading. A customized trainer should be inherited from the base trainer to implement customized functionality, e.g. `forward` at least.
- __train.py__  
  The main file to start training. Normally no need to change. 
- __utils.py__  
  Define some useful functions/classes. Normally no need to change.
  
To start training, run `train.py` like
```
python train.py -g 0,1 --vis
```
See all arguments by
```
python train.py -h
```

Once training is started, experiment configuration, training logs(open by tensorboard) and checkpoint models will be saved at `{exp_dir}`, which is soft-linked by `train_log` under current folder.
