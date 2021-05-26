#!/usr/bin/env python3

import yaml
import sys
import os
import gc
import logging
import pickle

import pandas as pd
import numpy as np
import lightgbm as lgb
from scipy.sparse import vstack, csr_matrix, load_npz
from sklearn.model_selection import StratifiedKFold

gc.enable()
# logger = logging.getLogger('brane')
# logger.setLevel(logging.DEBUG)

def train(model_name: str, eval_metric: int, max_depth: int, n_estimators:int, learning_rate: float, num_leaves: int, colsample_bytree: float, objective: str, use_local: bool, use_sampled_data: bool
) -> str:
    use_sampled_data_str = '1000' if use_sampled_data else ''
    data_loc_prefix = '../data/' if use_local else '/data/data/'
    model_name = f"{model_name}{use_sampled_data_str}"
  
    y_train = np.load(f'{data_loc_prefix}_train{use_sampled_data_str}.npy')
    train_ids = pd.read_pickle(f'{data_loc_prefix}_train_index{use_sampled_data_str}.pkl')
    n_splits = 5

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    skf.get_n_splits(train_ids, y_train)

    counter = 0
    #Transform data using small groups to reduce memory usage
    m = 100000
    n_splits = 5

    # logging.info('LightGBM')

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    skf.get_n_splits(train_ids, y_train)

    for train_index, test_index in skf.split(train_ids, y_train):
        
        # logger.info(f'Fold {counter + 1}')
        train = load_npz(f'{data_loc_prefix}_train{use_sampled_data_str}.npz')
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
                                        n_jobs=-1, silent=True)
        
        lgbm.fit(X_fit, y_fit, eval_metric=eval_metric, 
                    eval_set=[(X_val, y_val)], 
                    verbose=False, early_stopping_rounds=100)

                      
        # lgbm.booster_.save_model(f'{data_loc_prefix}boosters/{model_name}_{counter}.txt') 
        # model_str = lgbm.booster_.model_to_string()
        with open(f'{data_loc_prefix}boosters/{model_name}_{counter}.txt', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(lgbm, f, pickle.HIGHEST_PROTOCOL)


        counter += 1
        del X_fit, X_val, y_fit, y_val, train_index, test_index
        gc.collect()

    return "Model saved succesfully"


if __name__ == "__main__":
    command = sys.argv[1]
    model_name = os.environ["MODEL_NAME"]
    eval_metric = os.environ["EVAL_METRIC"]
    max_depth = int(os.environ["MAX_DEPTH"])
    n_estimators = int(os.environ["N_ESTIMATORS"])
    learning_rate = float(os.environ["LEARNING_RATE"])
    num_leaves = int(os.environ["NUM_LEAVES"])
    colsample_bytree = float(os.environ["COLSAMPLE_BYTREE"])
    objective = os.environ["OBJECTIVE"]
    use_local = os.environ["USE_LOCAL"] in ['true', 'True', True]
    use_sampled_data = os.environ["USE_SAMPLED_DATA"] in ['true', 'True', True]
    
    functions = {
    "train": train
    }
    output = functions[command](model_name, eval_metric, max_depth, n_estimators, learning_rate, num_leaves, colsample_bytree, objective, use_local, use_sampled_data)
    print(yaml.dump({"output": output}))
