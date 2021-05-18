import yaml
import sys
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np


#eval_metric: 
def preprocessing(Xtrain: str, ytrain: str, Xval: str, yval: str, modelname: str, eval_metric: int, max_depth: int, n_estimators:int, learning_rate: float, num_leaves: int, colsample_bytree: float, objective: str
) -> str:

   
    return "Preprocessed data"
   


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
