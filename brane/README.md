# Directory Structure

Only, the Python scripts (brane_preprocessing.py, brane_train.py, brane_predict.py) & the corresponding container.yml files, and the train.csv and test.csv are initially required to get started.

├── boosters

│   ├── lightgbm_0.txt

│   ├── lightgbm_1.txt

│   ├── lightgbm_2.txt

│   ├── lightgbm_3.txt

│   └── lightgbm_4.txt

├── data

│   ├── lgb_submission.csv

│   ├── sample_submission.csv

│   ├── test1000.csv

│   ├── test.csv

│   ├── _test_index.pkl

│   ├── _test.npz

│   ├── train1000.csv

│   ├── train.csv

│   ├── _train_index.pkl

│   ├── _train.npy

│   └── _train.npz
├── lightgbm_baseline.ipynb

├── predict

│   ├── brane_predict.py

│   ├── container.yml

│   └── env.example

├── preprocessing

│   ├── brane_preprocessing.py

│   ├── container.yml

│   └── env.example

├── set_env.sh

└── train

│   ├── brane_train.py

│   ├── container.yml

│   └── env.example


# Notes

train1000.csv and test1000.csv are files used for testing and checking if brane/directories are set up right because the regular files (train.csv, test.csv) take quite long to process. You can supply them as environment variables:

```bash
export PATH_TEST='data/test1000.csv' PATH_TRAIN='data/train1000.csv' 
```

For now, you also need to manually un/comment:

```python
submission = submission.sample(n=1000, random_state=1)
```

in brane_predict.py for the prediction package to work.
    