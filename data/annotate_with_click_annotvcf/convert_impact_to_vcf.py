from pysam import FastaFile
import pandas as pd
import sys

# This script convert impact raw data from .txt to .vcf, it takes two parameters:
# sys.argv[1] : input_file
# sys.argv[2] : output_file


# get reference genome file
ref = FastaFile('/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta')


# load impact, create vcf-like columns
impact = pd.read_csv(sys.argv[1], sep = '\t', low_memory = False)
impact = impact[['Chromosome', 'Start_Position', 'Reference_Allele', 'Tumor_Seq_Allele2']]

impact['ID']     = '.'
impact['QUAL']   = '.'
impact['FILTER'] = '.'
impact['INFO']   = "OLD_REF_ALT_POS=" + impact['Reference_Allele'] + '/' + impact['Tumor_Seq_Allele2'] + '/' + impact['Start_Position'].astype(str)
impact['FORMAT'] = '.'

impact = impact[['Chromosome', 'Start_Position', 'ID', 'Reference_Allele', 'Tumor_Seq_Allele2', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
impact.columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']


# modify every insertions REF and ALT columns (eg : -/A ⟹ T/TA)
# no changes made to POS column (it already refers to the position of the base before the insertion, eg T in the previous example)
is_insertion = impact.REF == '-'

def get_precedent_base_insertion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 1, end = start)

impact.loc[is_insertion,'REF'] = impact.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS), axis = 1)
impact.loc[is_insertion,'ALT'] = impact.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS) + x.ALT, axis = 1)


# modify every deletions REF and ALT columns (eg : A/- ⟹ TA/T)
# POS = POS - 1 to refer to the base just before the deletion eg T in the previous example (otherwise it would refer to the position of the first deleted base)
is_deletion = impact.ALT == '-'

def get_precedent_base_deletion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 2, end = start - 1)

impact.loc[is_deletion,'REF'] = impact.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS) + x.REF, axis = 1)
impact.loc[is_deletion,'ALT'] = impact.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS), axis = 1)
impact.loc[is_deletion,'POS'] -= 1


# drop duplicated mutations
impact.drop_duplicates(inplace = True)


# save .vcf
impact.to_csv(sys.argv[2], sep = '\t', index = False, header = False)
