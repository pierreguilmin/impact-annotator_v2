#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'

printf "${GREEN}→ Get the final IMPACT mutation data (~ 10 minutes)...${NO_COLOR}\n"
Rscript -e 'data_folder_path <- ".";source("../utils/r/compute_final_dataset.R");get_final_dataset()'
