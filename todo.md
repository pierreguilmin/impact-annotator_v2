# todo list

## General
- [ ] synonymous ?
- [ ] clean todo list

- Warning, dummy variables are also scaled!
https://github.com/seandavi/awesome-cancer-variant-databases/blob/master/README.md

## Git

- [ ] test the `README.md` links
- [ ] test the main `README.md` cloning link
- [ ] update `todo.md`
- [ ] instructions to download processed data
- [ ] sort `temp` folder
- [ ] `coding_mutations_analysis.ipynb`
- [ ] `oncokb_annotations_analysis.ipynb`
- [ ] `prediction/`
- [ ] re-run notebooks

- [ ] Specify `ssh-add` is necessary for anyone to use selene_job.ipy


## Machine Learning

- [ ] comment notebooks

### Sampling and cross-validation
- [ ] undersampling inconsistent sorted/shuffle
- [ ] Optimise undersampling/oversampling (imblearn technics)
- [ ] Unify patients and key for cross-validation? (http://scikit-learn.org/stable/modules/cross_validation.html#group-cv) -> Gfold repeated cross-validation

### Other
- [ ] Errors only appearing in detailed CV
- [ ] Rewrite `cluster_job_tutorial.ipynb` and add a section on how to use `Metrics` and `Summary`
- [ ] Metric representative of patient

### Ideas
- [ ] Deep learning
- [ ] Web interface
- [ ] More artefacts
- [ ] Data augmentation
- [ ] Polynomial regression: extending linear models with basis functions
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        print(X_poly.shape)
- [ ] Feature selection: https://github.com/amueller/scipy-2017-sklearn/blob/master/notebooks/19.Feature_Selection.ipynb
- [ ] More features ? (number of callers, caller flags...)
- [ ] COSMIC Peak arount mutation (Noushin idea)
- [ ] OncoKB likely oncogenic, predicted oncogenic: go back on this classification later on
- [ ] Call again the IMPACT `.bam` files with a uniform caller to perform analysis

