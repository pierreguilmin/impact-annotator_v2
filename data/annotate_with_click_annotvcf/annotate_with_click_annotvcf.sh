#!/bin/bash

GREEN='\033[0;32m'
NO_COLOR='\033[0m'

mkdir temp


##############################################
## convert .txt to .vcf ######################
##############################################
printf "${GREEN}→ Convert .txt to .vcf...${NO_COLOR}\n"

INPUT_FILE="../raw/all_IMPACT_mutations_20181105.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_20181105.vcf"

# custom Python script to convert impact from .txt to .vcf
python3 convert_impact_to_vcf.py $INPUT_FILE $OUTPUT_VCF

# create the .vcf header
sed -i '1s/^/##fileformat=VCFv4.2\n/' $OUTPUT_VCF
sed -i '2s/^/##INFO=<ID=OLD_REF_ALT_POS,Number=1,Type=String,Description="Old REF\/ALT\/POS values">\n/' $OUTPUT_VCF
sed -i '3s/^/#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n/' $OUTPUT_VCF

head $OUTPUT_VCF
cp $OUTPUT_VCF .
gzip $OUTPUT_VCF


##############################################
## annotate.vcf with click_annotvcf ##########
##############################################
printf "${GREEN}→ Annotate with click_annotvcf annotvcf (Juanes pipeline)...${NO_COLOR}\n"
click_annotvcf annotvcf \
--input_vcf $OUTPUT_VCF.gz \
--outdir temp \
--output_prefix annotvcf \
--assembly GRCH37D5 \
--reference /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta \
--vagrent /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/vagrent/Homo_sapiens_KnC.GRCh37.75.vagrent.cache.gz \
--vep-dir /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/vep/cache/ \
--ensembl-version 91 \
--custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_genomes/gnomad.genomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_genome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female \
--custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_exomes/gnomad.exomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_exome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female \
--custom /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81/CosmicMergedVariants.vcf.gz COSMIC GENE,STRAND,CDS,AA,CNT,SNP
#--cosmic /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81


##############################################
## clean #####################################
##############################################
printf "${GREEN}→ Clean...${NO_COLOR}\n"
mv temp/annotvcf.output.most_severe.tsv.gz ./click_annotvcf_IMPACT_mutations_20181105.txt.gz
gzip -d click_annotvcf_IMPACT_mutations_20181105.txt.gz
rm -rf temp

printf "${GREEN}→ Create header_click_annotvcf.txt...${NO_COLOR}\n"
grep '##' click_annotvcf_IMPACT_mutations_20181105.txt > header_click_annotvcf.txt
