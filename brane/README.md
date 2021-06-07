## Brane data processing pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4905892.svg)](https://doi.org/10.5281/zenodo.4905892)

#### Development

We use submodules for the individual packages of this repository. To clone the repository, run
```bash
git clone --recurse-submodules https://github.com/hkstm/UvA.WSCBS2021.git
```

or alternatively, run
```bash
git submodule init
git submodule update
```

#### Directory Structure

Only, the Python scripts (brane_preprocessing.py, brane_train.py, brane_predict.py) & the corresponding container.yml files, and the train.csv and test.csv are initially required to get started.

First run:

```bash
brane login http://localhost:8080 --username jovyan
```

Then run:

```bash
 make build 
```

to build and push all packages. At that point start an ide (make start-ide whereever brane's make file is) and upload your local brane/preprocessing/brane_preprocessing.ipynb to jupyters /data/preprocessing/ and brane/data/{train,test}1000.csv to /data/data/ and run the cells in brane_preprocessing.ipynb in jupyterlab to get started. This should take like max a minute and then return some bytecode.

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

#### Running the pipeline
After placing the data files in the right directory, and building the following packages with the Makefile, the `pipeline.ipynb` file can be opened up in the Brane IDE. Make sure to upload both the notebook and the necessary input files `test.csv`/`test1000.csv` and `train.csv`/`train1000.csv`. For further background info on brane, packages and coding we refer to the [documentation](https://docs.brane-framework.org/).

#### Kaggle module
For the kaggle module we refer to the directory containing a elaborate description in the Readme file [here](https://github.com/romnn/kaggle-brane/tree/a5f74e5a199365cea4178429e5adac8ca83523bc).

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
    
