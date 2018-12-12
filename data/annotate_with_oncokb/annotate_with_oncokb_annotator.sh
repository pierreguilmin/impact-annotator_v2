#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'


##############################################
## get the oncokb-annotator repository #######
##############################################
printf "${GREEN}→ Get the oncokb-annotator repo...${NO_COLOR}\n"
git clone https://github.com/oncokb/oncokb-annotator.git


##############################################
## prepare the IMPACT dataset ################
##############################################
printf "${GREEN}→ Prepare the final IMPACT mutation data 'final_IMPACT_mutations_20181105.txt' for oncokb-annotator...${NO_COLOR}\n"
Rscript prepare_for_annotation.R
head ready_to_annotate_final_IMPACT_mutations_20181105.txt


##############################################
## create a custom python virtualenv #########
##############################################
# create a 2.7 python virtualenv with the appropriate dependencies
source `which virtualenvwrapper.sh` # find the path to use virtualenvwrapper functions
printf "${GREEN}→ Create a python 2.7 virtual env...${NO_COLOR}\n"
mkvirtualenv --python=python2.7 oncokb-annotator_env
printf "${GREEN}→ Install matplotlib and its dependencies...${NO_COLOR}\n"
pip install matplotlib


##############################################
## launch oncokb-annotator ###################
##############################################
printf "${GREEN}→ Launch oncokb-annotator...${NO_COLOR}\n"
python oncokb-annotator/MafAnnotator.py -i 'ready_to_annotate_final_IMPACT_mutations_20181105.txt' -o 'oncokb_annotated_final_IMPACT_mutations_20181105.txt' > /dev/null


##############################################
## clean #####################################
##############################################
printf "${GREEN}→ Cleaning...${NO_COLOR}\n"
rm 'ready_to_annotate_final_IMPACT_mutations_20181105.txt'
rm -rf oncokb-annotator
# deactivate and remove the oncokb-annotator virtualenv
deactivate
rmvirtualenv oncokb-annotator_env
