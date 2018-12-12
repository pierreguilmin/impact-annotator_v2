# Get other databases data

To get the data run:
```shell
$ bash get_data.sh
```

The output files are:

* `CIViC_01-Jul-2018-VariantSummaries.tsv`: [CIViC](../../doc/biblio/variant_annotation_databases.md#civic) dataset (01/07/2018)  
Downoladed from https://civicdb.org/releases under "Variant Summaries/01-jul-2018"

* `CGI_catalog_of_validated_oncogenic_mutations.tsv`: [Cancer Genome Interpreter](../../doc/biblio/variant_annotation_databases.md#cancer-genome-interpreter) dataset (01/07/2018)  
Downloaded from https://www.cancergenomeinterpreter.org/mutations

* `allAnnotatedVariants.txt`: [OncoKB](../../doc/biblio/variant_annotation_databases.md#oncokb) dataset (up-to-date version)  
Downloaded from http://oncokb.org/api/v1/utils/allAnnotatedVariants.txt

* `PMK_IPM_Knowledgebase_Interpretations_Complete_20180807-1922.xlsx`: [Precision Medecine Knowledgebase](../../doc/biblio/variant_annotation_databases.md#precision-medicine-knowledgebase) dataset (up-to-date version)  
Downloaded from https://pmkb.weill.cornell.edu/therapies/download.xlsx

* `DoCM_variants.tsv`: [DocM](../../doc/biblio/variant_annotation_databases.md#docm) dataset (version 3.2 13/08/17)  
Downloaded from http://www.docm.info/api/v1/variants.tsv?versions=3.2

***

Two other files are already present in this folder (because they were not easily downladable with a script):

* `candl-results-20180809100701.csv`: [CanDL](../../doc/biblio/variant_annotation_databases.md#candl) dataset (09/08/2018)  
Downloaded from https://candl.osu.edu/download/full under "Export as CSV"

* `CancerGenesList.txt`: [OncoKB](../../doc/biblio/variant_annotation_databases.md#oncokb) genes list dataset (03/08/2018)  
Downloaded from http://oncokb.org/#/cancerGenes under "CANCER GENE LIST"