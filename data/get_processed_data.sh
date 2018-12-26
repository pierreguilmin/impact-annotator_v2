#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'


##############################################
## get IMPACT mutation annotated with VEP ####
##############################################
printf "${GREEN}→ Get the IMPACT mutation data annotated with VEP..."

# if in cluster we just copy the file, otherwise we scp
if (echo "$HOSTNAME" | grep -q "selene") || (echo "$HOSTNAME" | grep -q "luna")
then
    cp /home/guilminp/impact-annotator_v2/data/processed/final_IMPACT_mutations_20181105.txt processed/
    printf " done!${NO_COLOR}\n"
else
    printf "${NO_COLOR}\n"
    username=$1 # your luna username
    scp ${username}@selene.mskcc.org:/home/guilminp/impact-annotator_v2/data/processed/final_IMPACT_mutations_20181105.txt processed/
fi


##################################
## get final analysis dataset ####
##################################

printf "${GREEN}→ Get the final IMPACT mutation data used in the analysis..."

# if in cluster we just copy the file, otherwise we scp
if (echo "$HOSTNAME" | grep -q "selene") || (echo "$HOSTNAME" | grep -q "luna")
then
    cp /home/guilminp/impact-annotator_v2/data/processed/annotated_final_IMPACT_mutations_20181105.txt processed/
    printf " done!${NO_COLOR}\n"
else
    printf "${NO_COLOR}\n"
    username=$1 # your luna username
    scp ${username}@selene.mskcc.org:/home/guilminp/impact-annotator_v2/data/processed/annotated_final_IMPACT_mutations_20181105.txt processed/
fi
