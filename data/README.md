# Get the data

### Structure

* **`annotate_with_click_annotvcf/`**: this folder is used to annotate the raw dataset with click_annotvcf.  

* **`annotate_with_oncokb/`**: this folder is used to annotate the final curated dataset with oncokb-annotator.

* **`other_databases/`**: contains other databases than OncoKB.

* **`processed/`**: main processed data.

* **`raw/`**: main raw data.

***

The following explains how to download each dataset used in the study. More informations on the scripts and the outputs are given in the associated folders.  
:warning: Some dataset need other datasets to be computed, listed after "**Input:**". Please always check that you have the input datasets listed before trying to run the script to get the output dataset(s).

### Raw datasets and databases
- **Raw data stored in the cluster**  
    Input:   
    Outputs:  
    * `raw/all_IMPACT_mutations_20181105.txt` (raw dataset, IMPACT mutations data shared by Ahmet)

    Command:
    ```shell
    $ bash get_raw_data.sh your_cluster_username
    ```

- **Other databases pulled from internet ([`/other_databases`](other_databases/) folder)**  
    Input:  
    Outputs:  
    * `other_databases/CIViC_01-Jul-2018-VariantSummaries.tsv`
    * `other_databases/CGI_catalog_of_validated_oncogenic_mutations.tsv`
    * `other_databases/allAnnotatedVariants.txt`
    * `other_databases/PMK_IPM_Knowledgebase_Interpretations_Complete_20180807-1922.xlsx`
    * `other_databases/DoCM_variants.tsv`

    Command:
    ```shell
    $ cd other_databases
    $ bash get_data.sh
    ```

### Final dataset used in the rest of the study
> :zap: You can skip all this part by using the `get_processed_data.sh` script:
> - **Processed data stored in the cluster**  
>     Input:   
>     Outputs:
>     * `processed/final_IMPACT_mutations_20181105.txt` (final dataset annotated with VEP)  
>     * `processed/annotated_final_IMPACT_mutations_20181105.txt` (final dataset annotated with OncoKB and others → the one used for the analysis)
> 
>     Command:
>     ```shell
>     $ bash get_processed_data.sh your_cluster_username
>     ```

- **Raw dataset annotated with click_annotvcf ([`/annotate_with_click_annotvcf`](annotate_with_click_annotvcf/) folder)**  
    Input: `raw/all_IMPACT_mutations_20181105.txt`  
    Outputs:  
    * `annotate_with_click_annotvcf/all_IMPACT_mutations_20181105.vcf`  
    * `annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_20181105.txt`
    
    Command: :warning: run on cluster
    ```shell
    $ cd annotate_with_click_annotvcf
    $ bsub -o job_output.txt "bash annotate_with_click_annotvcf.sh"
    ```

- **Final dataset from the end of [`filter_and_process_raw_dataset.ipynb`](../analysis/compute_final_dataset/filter_and_process_raw_dataset.ipynb)**  
    Inputs:  
    * `annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_20181105.txt`
    * `annotate_with_click_annotvcf/all_IMPACT_mutations_20181105.vcf`   

    Output: `processed/final_IMPACT_mutations_20181105.txt`

    Command:  
    ```shell
    $ bash get_final_dataset.sh
    ```

- **Final dataset annotated with OncoKB ([`/annotate_with_oncokb_final_dataset`](annotate_with_oncokb/) folder)**  
    Input: `processed/final_IMPACT_mutations_20181105.txt`  
    Output: `annotate_with_oncokb/oncokb_annotated_final_IMPACT_mutations_20181105.txt`  
    
    Command: :warning: run on cluster
    ```shell
    $ cd annotate_with_oncokb_final_dataset
    $ bsub -We 20 -R select[internet] -o job_output.txt "bash annotate_with_oncokb_annotator.sh"
    ```

- **Final dataset from the end of [`annotate_final_dataset.ipynb`](../analysis/compute_final_dataset/annotate_final_dataset.ipynb)**  
    Input: `annotate_with_oncokb/oncokb_annotated_final_IMPACT_mutations_20181105.txt`  
    Output: `processed/annotated_final_IMPACT_mutations_20181105.txt`

    Command:  
    ```shell
    $ bash annotate_final_dataset.sh
    ```
