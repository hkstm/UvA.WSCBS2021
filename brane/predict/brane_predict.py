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
from scipy.sparse import csr_matrix, load_npz

gc.enable()
logger = logging.getLogger('brane')
logger.setLevel(logging.DEBUG)

data_loc_prefix = '/data/'  # do this when using jupyterlab/brane
# data_loc_prefix = '../'  # do this when testing locally

def predict(model_name: str) -> str:
    n_splits = 5

    test_ids  = pd.read_pickle(f'{data_loc_prefix}data/_test_index.pkl')
    lgb_test_result  = np.zeros(test_ids.shape[0])

    test = load_npz(f'{data_loc_prefix}data/_test.npz')
    test = csr_matrix(test, dtype='float32')

    for split in range(n_splits):
        with open(f'{data_loc_prefix}boosters/{model_name}_{split}.txt', 'rb') as f:
            lgbm = pickle.load(f)
        lgb_test_result += lgbm.predict_proba(test)[:,1]

    del test
    gc.collect()

    submission = pd.read_csv(f'{data_loc_prefix}data/sample_submission.csv')
    # submission = submission.sample(n=1000, random_state=1)
    submission['HasDetections'] = lgb_test_result / n_splits
    submission.to_csv(f'{data_loc_prefix}data/lgb_submission.csv', index=False)

    return "Made prediction"

if __name__ == "__main__":
    command = sys.argv[1]
    model_name = os.environ["MODEL_NAME"]
    functions = {
    "predict": predict
    }
    output = functions[command](model_name)
    print(yaml.dump({"output": output}))