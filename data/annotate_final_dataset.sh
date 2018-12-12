#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'

printf "${GREEN}→ Annotate the final dataset (~ 2 minutes)...${NO_COLOR}\n"
Rscript -e 'data_folder_path <- ".";source("../utils/r/compute_final_dataset.R");annotate_final_dataset()'
