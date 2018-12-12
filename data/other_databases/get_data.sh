#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'


##############################################
## get CIViC data ############################
##############################################
# Data downloaded from https://civicdb.org/releases under "Variant Summaries", 01/07/18 version
printf "${GREEN}→ Get the raw CIViC data...${NO_COLOR}\n"
curl https://civicdb.org/downloads/01-Jul-2018/01-Jul-2018-VariantSummaries.tsv --output "./CIViC_01-Jul-2018-VariantSummaries.tsv"


##############################################
## get Cancer Genome Interpreter data ########
##############################################
# Data downloaded from https://www.cancergenomeinterpreter.org/mutations, 01/17/18 version
printf "${GREEN}→ Get the raw Cancer Genome Interpreter data...${NO_COLOR}\n"
curl https://www.cancergenomeinterpreter.org/data/catalog_of_validated_oncogenic_mutations_latest.zip?ts=20180216 --output "./CGI_catalog_of_validated_oncogenic_mutations_latest.zip"
unzip CGI_catalog_of_validated_oncogenic_mutations_latest.zip
rm CGI_catalog_of_validated_oncogenic_mutations_latest.zip
rm README.txt
rm cancer_acronyms.txt
mv catalog_of_validated_oncogenic_mutations.tsv CGI_catalog_of_validated_oncogenic_mutations.tsv


##############################################
## get annotated variants from OncoKB ########
##############################################
# Data downloaded from http://oncokb.org/api/v1/utils/allAnnotatedVariants.txt, up-to-date version
printf "${GREEN}→ Get the raw OncoKB annotated variants data...${NO_COLOR}\n"
curl http://oncokb.org/api/v1/utils/allAnnotatedVariants.txt --output "./allAnnotatedVariants.txt"


##############################################
## get Precision Medecine Knowledge data #####
##############################################
# Data downloaded from https://pmkb.weill.cornell.edu/therapies/download.xlsx, up-to-date version
printf "${GREEN}→ Get the raw Precision Medecine Knowledge data...${NO_COLOR}\n"
curl https://pmkb.weill.cornell.edu/therapies/download.xlsx --output "./PMK_IPM_Knowledgebase_Interpretations_Complete_20180807-1922.xlsx"


##############################################
## get DoCM data #############################
##############################################
# Data downloaded from from http://www.docm.info/api/v1/variants.tsv?versions=3.2, version 3.2 (13/08/17)
printf "${GREEN}→ Get the raw DoCM data...${NO_COLOR}\n"
curl http://www.docm.info/api/v1/variants.tsv?versions=3.2 --output "./DoCM_variants.tsv"
