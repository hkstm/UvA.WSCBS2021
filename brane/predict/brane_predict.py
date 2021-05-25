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

def predict(model_name: str, use_local: bool, use_sampled_data: bool) -> str:
    use_sampled_data_str = '1000' if use_sampled_data else ''
    data_loc_prefix = '../data/' if use_local else '/data/data/'
    model_name = f"{model_name}{use_sampled_data_str}"
   
    n_splits = 5

    test_ids  = pd.read_pickle(f'{data_loc_prefix}_test_index{use_sampled_data_str}.pkl')
    lgb_test_result  = np.zeros(test_ids.shape[0])

    test = load_npz(f'{data_loc_prefix}_test{use_sampled_data_str}.npz')
    test = csr_matrix(test, dtype='float32')

    for split in range(n_splits):
        with open(f'{data_loc_prefix}boosters/{model_name}_{split}.txt', 'rb') as f:
            lgbm = pickle.load(f)
        lgb_test_result += lgbm.predict_proba(test)[:,1]

    del test
    gc.collect()

    submission = pd.read_csv(f'{data_loc_prefix}sample_submission{use_sampled_data_str}.csv')
    submission['HasDetections'] = lgb_test_result / n_splits
    submission.to_csv(f'{data_loc_prefix}lgb_submission{use_sampled_data_str}.csv', index=False)

    return "Made prediction"

if __name__ == "__main__":
    command = sys.argv[1]
    model_name = os.environ["MODEL_NAME"]
    use_local = os.environ["USE_LOCAL"]
    use_sampled_data = os.environ["USE_SAMPLED_DATA"]
    functions = {
    "predict": predict
    }
    output = functions[command](model_name, use_local, use_sampled_data)
    print(yaml.dump({"output": output}))
