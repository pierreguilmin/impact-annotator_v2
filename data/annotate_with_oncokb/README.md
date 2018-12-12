# Annotate the mutations with oncokb-annotator

To annotate the cleaned dataset `cleaned_IMPACT_mutations_180508.txt` with the oncokb annotations from [oncokb-annotator](https://github.com/oncokb/oncokb-annotator) run:  
:warning: run on cluster
```bash
$ bsub -We 30 -R select[internet] -o job_output.txt "bash annotate_with_oncokb_annotator.sh"
```

The output files are:
* `oncokb_annotated_final_IMPACT_mutations_20181105.txt`, the annotated version.
* `job_output.txt` the output of the job

The CPU time on the cluster was 1,382 seconds (≈ 23 minutes).

***

### Details

We use [oncokb-annotator](https://github.com/oncokb/oncokb-annotator) to annotate the dataset.

The script [`annotate_with_oncokb_annotator.sh`](annotate_with_oncokb_annotator.sh) does the following:

* Clone the repository at https://github.com/oncokb/oncokb-annotator:
```bash
git clone https://github.com/oncokb/oncokb-annotator.git
```

* Call [`prepare_for_annotation.R`](prepare_for_annotation.R) which does some minor changes on the dataset. Indeed oncokb-annotator needs a `Variant_Classification` feature, which can be computed from the `VEP_Consequence` feature as follow:

| VEP_Consequence           | Variant_Classification |
| ------------------------- | ---------------------- |
| missense_variant          | Missense_Mutation      |
| frameshift_variant        | <sup>*</sup> see under |
| stop_gained               | Nonsense_Mutation      |
| splice_acceptor_variant   | Splice_Site            |
| inframe_deletion          | In_Frame_Del           |
| splice_donor_variant      | Splice_Site            |
| inframe_insertion         | In_Frame_Ins           |
| start_lost                | Start_Codon_Del        |
| stop_lost                 | Nonstop_Mutation       |  

<sup>* </sup> To get the `Variant_Classification` for `frameshift_variant`, the following rules where applied:

* if `VEP_VARIANT_CLASS == "insertion"` → `Frame_Shift_Ins`
* if `VEP_VARIANT_CLASS == "deletion"` → `Frame_Shift_Del`
* if `VEP_VARIANT_CLASS == "delins"` → `Frame_Shift_Del`

Actually these subcases are useless, because oncokb-annotator considers all these variants as "truncating mutations".

* Create a python2.7 virtualenv named `oncokb-annotator-env` and install matplotlib (needed by oncokb-annotator). This virtualenv will be removed at the end of the script:
```bash
mkvirtualenv --python=python2.7 oncokb-annotator_env
pip install matplotlib

# ... further

deactivate
rmvirtualenv oncokb-annotator_env
```

* Run oncokb-annotator.

* Do some cleaning (remove temporary files and the oncokb-annotator repository).
