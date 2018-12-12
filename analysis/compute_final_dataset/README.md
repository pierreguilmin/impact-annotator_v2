# Compute final dataset

### List of all the notebooks

- **`filter_and_process_raw_dataset.ipynb`**  
This notebook computes the final dataset from the raw impact dataset, the final dataset will be used everywhere else in the analysis. It combines a lot of knowledge from a previous study to filter, clean, curate and annotate the raw dataset. All the operations are summarised in the `utils/r/compute_final_dataset.R` R script and can be applied on the raw dataset by using the `get_final_dataset()` function.  
⚠️ This notebook is long, technical (*and a bit boring*), we wouln't advise you to read it to begin with the dataset understanding...

- **`annotate_final_dataset.ipynb`**  
This notebook annotates the final dataset obtained at the end of `filter_and_process_raw_dataset.ipynb` by adding some features. All the operations are summarised in the `utils/r/compute_final_dataset.R` R script and can be applied on the final dataset by using the `annotate_final_dataset()` function.
