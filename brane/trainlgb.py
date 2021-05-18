import lightgbm as lgb
import pandas as pd
import numpy as np
from pandas import DataFrame
import yaml
import sys
import os

from lightgbm import LGBMClassifier

#eval_metric: 
def fit_lgb(Xtrain: str, ytrain: str, Xval: str, yval: str, eval_metric: int, max_depth: int, n_estimators:int, learning_rate: float, num_leaves: int, colsample_bytree: float, objective: str
) -> str:
    Xtrain = pd.read_pickle(Xtrain)
    ytrain = pd.read_pickle(ytrain)
    Xval = pd.read_pickle(Xval)
    yval = pd.read_pickle(yval)

    
    lgb = lgb.LGBMClassifier(max_depth=max_depth,
                                   n_estimators=n_estimators,
                                   learning_rate=learning_rate,
                                   num_leaves=num_leaves,
                                   colsample_bytree=colsample_bytree,
                                   objective=objective, 
                                   n_jobs=-1)
      
    lgb.fit(Xtrain, ytrain, eval_metric=eval_metric, 
                  eval_set=[(Xval, yval)], 
                  verbose=100, early_stopping_rounds=100)

    # Save also on the FileSystem /data as pickle string
    stringmodel = lgb.model_to_string()
    return stringmodel


if __name__ == "__main__":
  command = sys.argv[1]
  xtrain = os.environ["XTRAIN"]
  ytrain = os.environ["YTRAIN"]
  xval = os.environ["XVAL"]
  yval = os.environ["YVAL"]
  eval_metric = os.environ["EVAL_METRIC"]
  max_depth = os.environ["MAX_DEPTH"]
  n_estimators = os.environ["N_ESTIMATORS"]
  learning_rate = os.environ["LEARNING_RATE"]
  num_leaves = os.environ["NUM_LEAVES"]
  colsample_bytree = os.environ["COLSAMPLE_BYTREE"]
  objective = os.environ["OBJECTIVE"]
  functions = {
    "fit": fit_lgb
    
  }
  output = functions[command](xtrain, ytrain, xval, yval, eval_metric, max_depth, n_estimators, learning_rate, num_leaves, colsample_bytree, objective)
  print(yaml.dump({"output": output}))
