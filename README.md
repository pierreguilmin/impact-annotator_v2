:construction: *work in progress* :construction:

# impact-annotator

**Develop a knowledge-based approach using MSK-IMPACT data to build an automatic variant classifier.**

***

## Repository structure

- **`analysis/`**: folder to design and run the analysis, contains several sub-folders:
    - `compute_final_dataset/`: this part is written in R and describes all the process to compute the final dataset from the raw IMPACT dataset. The final dataset will be used in the rest of the analysis.
    - `description/`: this part is written in R and contains some description/analysis of the dataset.
    - `prediction/`: this part is written in Python and explains the classifier building process.

- **`data/`**: raw data and main processed data, processed data should be reproducible from raw data.   
  > :warning: This folder should not be versionned.

- **`doc/`**: useful documentation, bibliography, slides for talks...

- **`temp/`**: drafts, temporary files and old scripts.  

- **`utils/`**: main scripts used across analysis.




## Working with this repository

### Clone the repository

To clone this repository on your local computer please run:
```shell
$ git clone https://github.com/PierreGuilmin/impact-annotator.git
```

### Step 1 - Setup your R environment
The first part of the repository was written and tested under `R 3.5.1` and `R 3.2.3`, working with JupyterLab.

To work with this repository please make sure to have the following R packages installed:

- `tidyverse`
- `gridExtra`
- `utf8`
- `readxl`
- `hexbin`

```R
# run in an R console
install.packages('tidyverse', repos = 'http://cran.us.r-project.org')
install.packages('gridExtra', repos = 'http://cran.us.r-project.org')
install.packages('utf8',      repos = 'http://cran.us.r-project.org')
install.packages('readxl',    repos = 'http://cran.us.r-project.org')
install.packages('hexbin',    repos = 'http://cran.us.r-project.org')
```

### Step 2 - Setup your Python environment
The second part of the repository was written and tested under `Python 3.6`, working with JupyterLab. You can see the requirements under [`conda-env_requirements.yml`](conda-env_requirements.yml). The main Python packages used are:

- `ipython`
- `nb_conda_kernels`
- `numpy`
- `matplotlib`
- `seaborn`
- `pandas`
- `scikit-learn`
- `imbalanced-learn`

#### Step 2.1 - Setup a python virtualenv on the cluster

To create the virtualenv used by the jobs, please run the following commands on your selene cluster session:
```bash
# create the virtualenv
$ mkvirtualenv --python=python3.6 imp-ann_env
# install useful libraries
$ pip install ipython numpy matplotlib seaborn pandas scikit-learn imbalanced-learn
```

Some useful command lines:
```bash
# activate the virtualenv
$ workon impact-annotator_env

# deactivate the virtualenv
$ deactivate

# remove the virtualenv
$ rmvirtualenv imp-ann_env
```

On the cluster, please add the following line in your `~/.bash_profile` to use virtualenv functions directly from the notebook later:
```bash
# add in your cluster ~/.bash_profile
source `which virtualenvwrapper.sh`
```

#### Step 2.2 - Setup a python conda-environment on your local computer

We assume you have conda installed on your computer, otherwise please see https://conda.io/docs/index.html (conda documentation) and https://conda.io/docs/_downloads/conda-cheatsheet.pdf (conda cheat sheet). You need to install `jupyter lab` and `nb_conda_kernels` in your base conda environment if not done yet.

To create the conda-env, please run the following command:
```bash
# create the conda-env and install the appropriate libraries
$ conda env create --name imp-ann_env --file conda-env_requirements.yml
```

Some useful command lines to work with this conda-env:
```bash
# activate the conda-env
$ source activate imp-ann_env

# deactivate the conda-env
$ source deactivate

# remove the conda-env
$ conda env remove --name imp-ann_env
```

> :warning: Please always activate the `imp-ann_env` conda-env before running any Python notebook, to make sure you have all the necessary dependencies and the good libraries version:
> ```bash
> # if you use jupyter notebook
> $ source activate imp-ann_env; jupyter notebook
> 
> # if you use jupyter lab
> $ source activate imp-ann_env; jupyter lab
> ```

In any Python Jupyter notebook, importing the file `utils/python/setup_environment.ipy` automatically checks that you're running the notebook under the `imp-ann_env` conda-env, you can check it yourself by running in the notebook:
```ipython
# prints the current conda-env used
!echo $CONDA_DEFAULT_ENV

# list all the conda-env on your computer, the one you're working on is indicated by a star
!conda env list
```

### Step 3 - Download the data
Go to the [`data/`](data/) folder and follow the `README.md` to download all the necessary data.

### Step 3: Checklist
- [ ] Download R packages `tidyverse`, `gridExtra`, `utf8`, `readxl`, `hexbin`
- [ ] Create cluster virtualenv `imp-ann_env`
- [ ] Add <code>source \`which virtualenvwrapper.sh\`</code> in cluster `~/.bash_profile`
- [ ] Create local conda-env `imp-ann_env`
- [ ] Remember to always activate the conda-env `imp-ann_env` before running a Jupyter Notebook/JupyterLab instance locally (`$ source activate imp-ann_env`)




## Details on the notebooks
All R notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../utils/r/custom_tools.R")
setup_environment("../../utils/r")
```

All Python notebooks will begin with the following lines, which load a set of custom function designed by us, and load appropriate libraries, it also makes sure that you're working on the `imp-ann_env` that you should have created earlier:
```ipython
%run ../../utils/Python/setup_environment.ipy

# if you want to send jobs on the cluster from the notebook on your local computer, please also run something like the following:
# (see analysis/prediction/cluster_job_tutorial.ipynb for more informations)
%run ../../utils/Python/selene_job.ipy
Selene_Job.cluster_username             = 'guilminp'
Selene_Job.ssh_remote_jobs_cluster_path = '/home/guilminp/impact-annotator_v2/analysis/prediction/artefact_classification/ssh_remote_jobs'
Selene_Job.ssh_remote_jobs_local_path   = 'ssh_remote_jobs'
```




## Supplementary
The conda-env and the `.yml` requirement file were created with the following commands:
```bash
# create conda-env
conda create -c conda-forge --name imp-ann_env python=3.6 ipython nb_conda_kernels numpy matplotlib seaborn pandas scikit-learn imbalanced-learn

# export requirements as .yml
conda env export > conda-env_requirements.yml
```

🕰 This work is based on a previous working directory that you can find at https://github.com/ElsaB/impact-annotator. We decided to reformat this directory to make it easier to use (the previous directory was based on two different versions of IMPACT). No worries, all the relevant previous work is included and documented in this directory and you shouldn't have to go back to the previous one.  
The decision has been made at the end of the previous work to keep the VEP annotation for IMPACT mutations, more consistent, up-to-date and robust than the given IMPACT annotation. The choice-making process is described in some of the notebooks of the old repository.
