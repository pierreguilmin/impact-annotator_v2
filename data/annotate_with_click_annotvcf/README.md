# Annotate the mutations with the click_annotvcf pipeline

To annotate the raw dataset `all_IMPACT_mutations_20181105.txt` with the [click_annotvcf](https://github.com/leukgen/click_annotvcf) pipeline run:  
:warning: run on cluster
```bash
$ bsub -o job_output.txt "bash annotate_with_click_annotvcf.sh"
```

The output files are:
* `click_annotvcf_IMPACT_mutations_20181105.txt`, the annotated version
* `all_IMPACT_mutations_20181105.vcf`, the `.vcf` file after conversion
* `header_click_annotvcf.txt` the header of `click_annotvcf_IMPACT_mutations_20181105.txt`, explaining the meaning of every column name 
* `job_output.txt` the output of the job

The CPU time on the cluster was 12,880 (≈ 3.6 hours).

***

### Details

We use [click_annotvcf](https://github.com/leukgen/click_annotvcf) to annotate the dataset. The script [`annotate_with_click_annotvcf.sh`](annotate_with_click_annotvcf.sh) does the following:

* Create a `.vcf` file from the raw data by calling [`convert_impact_to_vcf.py`](convert_impact_to_vcf.py)
```bash
INPUT_FILE="../raw/all_IMPACT_mutations_20181105.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_20181105.vcf"

# custom Python script to convert impact from .txt to .vcf
python3 convert_impact_to_vcf.py $INPUT_FILE $OUTPUT_VCF

sed -i '1s/^/##fileformat=VCFv4.2\n/' $OUTPUT_VCF
sed -i '2s/^/##INFO=<ID=OLD_REF_ALT_POS,Number=1,Type=String,Description="Old REF\/ALT\/POS values">\n/' $OUTPUT_VCF
sed -i '3s/^/#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n/' $OUTPUT_VCF
```
> See in next section a quick review of what the script [`convert_impact_to_vcf.py`](convert_impact_to_vcf.py) does and why we chose to create the `.vcf` by hand instead of using the maf2vcf script of the [vcf2maf](https://github.com/mskcc/vcf2maf) repository.

* Run `click_annotvcf annotvcf`.
```bash
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
--custom /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81/CosmicMergedVariants.vcf.gz COSMIC GENE,STRAND,CDS,AA,CNT,SNP \
#--cosmic /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81
```
The cosmic annotations were removed from the call to click_annotvcf as it made the file grow from ≈ 500 MB to 44 GB.

* Do some cleaning (remove temporary files).

### `convert_impact_to_vcf.py` vs vcf2maf
[**`convert_impact_to_vcf.py`**](convert_impact_to_vcf.py) The script does the following:

* Load impact from the given input file and create vcf-like columns
* Modify `INS` and `DEL` mutations to match `.vcf` format, for example:
	* `INS`: `-/A` ⟹ `T/TA`
	* `DEL`: `A/-` ⟹ `TA/T` and `POS` corrected
* Remove duplicated rows
* Save the `.vcf` impact as the given output file
* The old `REF`, `ALT` and `POS` fields are stored in the `INFO` field of the `.vcf`

**`maf2vcf.pl`**

To convert our dataset to `.vcf` we also tried to use the `maf2vcf.pl` script of the [vcf2maf](https://github.com/mskcc/vcf2maf) repository. However, we faced two problems that lead us to do our own script:

* The resulting `.vcf` was heavy to work on as each mutation is unnecessarily linked to its `Tumor_Sample_Barcode`, thus adding more than 20,000 extra columns to the `.vcf` file (due to our ≈20,000 `Tumor_Sample_Barcode` in impact).
* The processing to create the `.vcf` file was way longer.

See the script used to clone the vcf2maf repository and apply `maf2vcf.pl` on impact:

```bash
GREEN='\033[0;32m'
NO_COLOR='\033[0m'

mkdir temp

INPUT_FILE="../raw/all_IMPACT_mutations_20181105.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_20181105.vcf"

printf "\n${GREEN}-> Get the vcf2maf repo...${NO_COLOR}\n"
export VCF2MAF_URL=`curl -sL https://api.github.com/repos/mskcc/vcf2maf/releases | grep -m1 tarball_url | cut -d\" -f4`
curl -L -o temp/mskcc-vcf2maf.tar.gz $VCF2MAF_URL
tar -zxf temp/mskcc-vcf2maf.tar.gz --directory temp

printf "\n${GREEN}-> Convert .txt to .vcf...${NO_COLOR}\n"
perl temp/mskcc-vcf2maf-decbf60/maf2vcf.pl --input-maf $INPUT_FILE --output-dir temp --ref-fasta /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta

cp $OUTPUT_VCF .
```
