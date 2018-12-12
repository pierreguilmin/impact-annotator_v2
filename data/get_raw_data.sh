#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'

printf "${GREEN}→ Get the raw IMPACT mutation data..."

# if in cluster we just copy the file, otherwise we scp
if (echo "$HOSTNAME" | grep -q "selene") || (echo "$HOSTNAME" | grep -q "luna")
then
	cp /ifs/res/papaemme/users/eb2/impact_mutations/all_IMPACT_mutations_20181105.txt raw/
    printf " done!${NO_COLOR}\n"
else
    printf "${NO_COLOR}\n"
	username=$1 # your luna username
	scp ${username}@selene.mskcc.org:/ifs/res/papaemme/users/eb2/impact_mutations/all_IMPACT_mutations_20181105.txt raw/
fi
