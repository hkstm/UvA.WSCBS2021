#!/usr/bin/env python3

import yaml
import sys
import os
import gc
import logging

import pandas as pd
import numpy as np
import lightgbm as lgb
from scipy.sparse import vstack, csr_matrix, load_npz
from sklearn.model_selection import StratifiedKFold

gc.enable()
logger = logging.getLogger('brane')
logger.setLevel(logging.DEBUG)


# #eval_metric: 
# def fit_lgb(Xtrain: str, ytrain: str, Xval: str, yval: str, modelname: str, eval_metric: int, max_depth: int, n_estimators:int, learning_rate: float, num_leaves: int, colsample_bytree: float, objective: str
# ) -> str:
#     Xtrain = pd.read_pickle(Xtrain)
#     ytrain = pd.read_pickle(ytrain)
#     Xval = pd.read_pickle(Xval)
#     yval = pd.read_pickle(yval)

    # lgbm = lgb.LGBMClassifier(max_depth=max_depth,
    #                                 n_estimators=n_estimators,
    #                                 learning_rate=learning_rate,
    #                                 num_leaves=num_leaves,
    #                                 colsample_bytree=colsample_bytree,
    #                                 objective=objective, 
    #                                 n_jobs=-1)
    
    # lgbm.fit(Xtrain, ytrain, eval_metric=eval_metric, 
    #             eval_set=[(Xval, yval)], 
    #             verbose=100, early_stopping_rounds=100)


#     lgbm.save_model('data/{}.txt'.format(modelname), num_iteration=lgbm.best_iteration) 

#     return "Model saved succesfully"

def fit_lgb(model_name: str, eval_metric: int, max_depth: int, n_estimators:int, learning_rate: float, num_leaves: int, colsample_bytree: float, objective: str
) -> str:

    y_train = np.load('data/_train.npy')
    train_ids = pd.read_pickle('data/_train_index.pkl')
    n_splits = 5

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    skf.get_n_splits(train_ids, y_train)

    counter = 0
    #Transform data using small groups to reduce memory usage
    m = 100000
    n_splits = 5

    logging.info('LightGBM')

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    skf.get_n_splits(train_ids, y_train)

    for train_index, test_index in skf.split(train_ids, y_train):
        
        logger.info(f'Fold {counter + 1}')
        train = load_npz('data/_train.npz')
        X_fit = vstack([train[train_index[i*m:(i+1)*m]] for i in range(train_index.shape[0] // m + 1)])
        X_val = vstack([train[test_index[i*m:(i+1)*m]]  for i in range(test_index.shape[0] //  m + 1)])
        X_fit, X_val = csr_matrix(X_fit, dtype='float32'), csr_matrix(X_val, dtype='float32')
        y_fit, y_val = y_train[train_index], y_train[test_index]
    
        
        del train
        gc.collect()

        lgbm = lgb.LGBMClassifier(max_depth=max_depth,
                                        n_estimators=n_estimators,
                                        learning_rate=learning_rate,
                                        num_leaves=num_leaves,
                                        colsample_bytree=colsample_bytree,
                                        objective=objective, 
                                        n_jobs=-1)
        
        lgbm.fit(X_fit, y_fit, eval_metric=eval_metric, 
                    eval_set=[(X_val, y_val)], 
                    verbose=100, early_stopping_rounds=100)

                      
        lgbm.save_model(f'models/{model_name}_{counter}.txt', num_iteration=lgbm.best_iteration) 
        counter += 1
        del X_fit, X_val, y_fit, y_val, train_index, test_index
        gc.collect()

        return "Model saved succesfully"


if __name__ == "__main__":
    command = sys.argv[1]
    # xtrain = os.environ["XTRAIN"]
    # ytrain = os.environ["YTRAIN"]
    # xval = os.environ["XVAL"]
    # yval = os.environ["YVAL"]
    model_name = os.environ["MODEL_NAME"]
    eval_metric = os.environ["EVAL_METRIC"]
    max_depth = os.environ["MAX_DEPTH"]
    n_estimators = os.environ["N_ESTIMATORS"]
    learning_rate = os.environ["LEARNING_RATlgbmE"]
    num_leaves = os.environ["NUM_LEAVES"]
    colsample_bytree = os.environ["COLSAMPLE_BYTREE"]
    objective = os.environ["OBJECTIVE"]
    functions = {
    "fit": fit_lgb
    }
    # output = functions[command](xtrain, ytrain, xval, yval, eval_metric, max_depth, n_estimators, learning_rate, num_leaves, colsample_bytree, objective)
    output = functions[command](model_name, eval_metric, max_depth, n_estimators, learning_rate, num_leaves, colsample_bytree, objective)

    logger.info(yaml.dump({"output": output}))
