# todo list

## Git
- [x] test the GitHub links
- [x] test the main `README.md` cloning link
- [x] rename repository
- [x] clean `todo.md` list
- [x] specify `ssh-add` is necessary for anyone to use `selene_job.ipy`
- [x] add instructions to download processed data directly
- [x] commit `metrics.pkl`, `script.ipy` and `job_output.txt` from every job



## Final clean
- [x] sort `temp/` folder
- [x] plot features importance in feature engineering related notebooks
- [ ] comment all `prediction/` notebooks



## Machine Learning

### Sampling and cross-validation
- [ ] inconsistent sorted vs shuffle results
- [ ] optimise undersampling/oversampling strategy (imblearn technics)

### Other
- [x] try 3-base change feature
- [ ] try features like (BioC)
        - genome mappability
        - repeat level
        - GC content

### Ideas
- [ ] get more artefacts
- [ ] find metric representative of patient
- [ ] COSMIC Peak arount mutation (Noushin idea)
- [ ] call again the IMPACT `.bam` files with a uniform caller to perform analysis



## Python
- [x] virutalenvwrapper sourcing in `~/.bash_profile` and not `~/.bashrc`
- [x] simplify cluster username, and ssh_remote_jobs path specification for `Selene_Job` class
- [x] add `get_local_results()` to `Selene_Job`



## Roadmap

1. 📋Compare the prediction results with original classification (consistent/inconsistent somatic/non-somatic annotation OR oncogenic vs likely oncogenic vs predicted oncogenic classification).  
3. 🔬Try **basic** deep learning methods.  
4. 👀Compare both steps (artefact vs somatic and driver vs passenger) with existing methods.  
5. 🌍Create a two-steps web-based classifier.  
6. 📃Write the paper!  
