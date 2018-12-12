# Variant annotation databases

Also see https://github.com/seandavi/awesome-cancer-variant-databases/blob/master/README.md.

**Summary and table of contents**

| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [MyCancerGenome](#mycancergenome)                                     | ?        | ?     | -        | :x:                | :x:                     | 2013             | https://www.mycancergenome.org               |
| [CanDL](#candl)                                                       | 330      | 56    | 2015     | :white_check_mark: | :white_check_mark:      | 2015             | https://candl.osu.edu                        |
| [JAX-Clinical Knowledgebase](#jax-clinical-knowledgebase)             | ?        | 82    | 08/08/18 | :x:                | :x:                     | 2016             | https://ckb.jax.org                          |
| [DoCM](#docm)                                                         | 1,364    | 132   | 13/08/18 | :white_check_mark: | :white_check_mark:      | 2016             | http://www.docm.info                         |
| [Precision Medicine Knowledgebase](#precision-medicine-knowledgebase) | 2,168    | 606   | 08/08/18 | :white_check_mark: | :x:                     | 2016             | https://pmkb.weill.cornell.edu               |
| [CIViC](#civic)                                                       | 1,936    | 358   | 08/08/18 | :white_check_mark: | :white_check_mark:      | 2017             | https://civicdb.org/home                     |
| [OncoKB](#oncokb)                                                     | 3,971    | 477   | 09/08/18 | :white_check_mark: | -                       | 2017             | http://oncokb.org/#/                         |
| [Personalized Cancer Therapy](#personalized-cancer-therapy)           | ?        | ?     | -        | :x:                | :x:                     | 2017             | https://pct.mdanderson.org                   |
| [Cancer Genome Interpreter](#cancer-genome-interpreter)               | 5,601    | 765   | 08/08/18 | :white_check_mark: | :white_check_mark:      | 2018             | https://www.cancergenomeinterpreter.org/home |

*This is not an exhaustive list.*  

See the notebook [`analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb`](../../analysis/description/comparison_between_variant_annotation_databases.ipynb) for direct comparison between some of these databases and OncoKB (when the data was available and usable, cf. "results in the notebook" column in the above table).



***



## MyCancerGenome
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [MyCancerGenome](#mycancergenome)                                     | ?        | ?     | -        | :x:                | :x:                     | 2013             | https://www.mycancergenome.org               |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4121886/) Yeh P, Chen H, Andrews J, Naser R, Pao W, Horn L. DNA-Mutation Inventory to Refine and Enhance Cancer Treatment (DIRECT): A Catalog of Clinically Relevant Cancer Mutations to Enable Genome-Directed Anticancer Therapy. Clinical cancer research : an official journal of the American Association for Cancer Research. 2013;19(7):1894-1901.  doi:10.1158/1078-0432.CCR-12-1894.  

* **What is it?** My Cancer Genome is a precision cancer medicine knowledge resource for physicians, patients, caregivers and researchers. It gives information on what mutations make cancers grow and related therapeutic implications, including available clinical trials.
* **Where does the data comes from?** A database (DIRECT: 'DNA-mutation Inventory to Refine and Enhance Cancer Treatment') has been established, it contains information about the potential clinical significance of specific tumor mutations. To compile the information in DIRECT, the PCMI team used a retrospective PubMed medical subject heading (MeSH) search to identify patient-level, mutation-specific, drug response data from different studies in NSCLC. The initial goal of the DIRECT database was to catalogue clinically relevant somatic mutations in lung cancer. The project began by cataloguing data from patients with EGFR mutations but will be expanding to incorporate data on all known mutations with potential clinical significance in various types of cancer.  Not sure if DIRECT is the only database used, the website says "Currently, DIRECT catalogues drug response data from patients with non-small cell lung cancer (NSCLC) whose tumors harbor mutations in EGFR", but maybe the website is not up-to-date. Indeed, we can find other cancer type variants on the website.
* **Other informations**
    * Focused on "patient focus content".



## CanDL
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [CanDL](#candl)                                                       | 330      | 56    | 2015     | :white_check_mark: | :white_check_mark:      | 2015             | https://candl.osu.edu                        |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4597274/) Damodaran S, Miya J, Kautto E, et al. Cancer Driver Log (CanDL): Catalog of Potentially Actionable Cancer Mutations. The Journal of Molecular Diagnostics : JMD. 2015;17(5):554-559. doi:10.1016/j.jmoldx.2015.05.002.  

* **What is it?** Expert-curated database of potentially actionnable driver mutations.
* **Where does the data comes from?** Review scientific literature to identify variants that have been functionnaly characterized in vitro and in vivo as driver mutations. Mechanism for third-party contributions. Curated mutations from the list of genes from the Sanger Cancer Gene Census. Requirements to qualify as a driver mutation: include in vivo or in vitro experimentation. No update made to the database without manual expert review.
* **Other informations**
    * The most recent update to data was on 5:15pm, July 31st, 2015.
    * Only single-nucleotide substitutions in oncogenes



## JAX-Clinical Knowledgebase
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [JAX-Clinical Knowledgebase](#jax-clinical-knowledgebase)             | ?        | 82    | 08/08/18 | :x:                | :x:                     | 2016             | https://ckb.jax.org                          |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pubmed/26772741) Patterson SE, Liu R, Statz CM, Durkin D, Lakshminarayana A, Mockus SM. The clinical trial landscape in oncology and connectivity of somatic mutational profiles to targeted therapies. Human Genomics. 2016;10:4. doi:10.1186/s40246-016-0061-7.  

* **What is it?** Identification and annotation of clinically relevant cancer variants.  
* **Where does the data comes from?** FDA-approved therapy or targeted therapy in clinical trials. Data dynamically curated by experts. In-house databse (the JAX Clinical Knowledgebase JAX-CKB): semi-automated/manually curated database of gene/variant annotations, therapy knowledge, diagnostic/prognostic information, and clinical trials related to oncology.  
* **Other informations**
    * Filtering to ensure the high-quality somatic variations: low coverage, vaf, silent mutations, likely germline, outside of coding regions
    * All types of mutations



## DoCM
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [DoCM](#docm)                                                         | 1,364    | 132   | 13/08/18 | :white_check_mark: | :white_check_mark:      | 2016             | http://www.docm.info                         |

**Paper:** [link](https://www.nature.com/articles/nmeth.4000) Ainscough BJ, Griffith M, Coffman AC, et al. DoCM: a database of curated mutations in cancer. Nature methods. 2016;13(10):806-807. doi:10.1038/nmeth.4000.

* **What is it?** Highly curated database of known, disease-causing mutations that provides easily explorable variant lists with direct links to source citations for easy verification.
* **Where does the data comes from?** Curation of the litterature, CIViC, Drug Gene Knowledge Base, My Cancer Genome, ... by disease experts. Criteria for inclusion: clinical relevance (drug targets associated with the mutation, diagnostic or prognostic markers associated with the mutation), functional evidence (disease function described in cell lines, disease function described in animal models, extremely recurrent mutation coupled with expert opinion of the significance of the mutation). Batches can be submitted by anyone.



## Precision Medicine Knowledgebase
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [Precision Medicine Knowledgebase](#precision-medicine-knowledgebase) | 2168     | 606   | 08/08/18 | :white_check_mark: | :x:                     | 2016             | https://pmkb.weill.cornell.edu               |

**Article:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5391733/) Huang L, Fernandes H, Zia H, et al. The cancer precision medicine knowledge base for structured clinical-grade mutations and interpretations. Journal of the American Medical Informatics Association : JAMIA. 2017;24(3):513-519. doi:10.1093/jamia/ocw148.  

* **What is it?** Interactive online application for collaborative editing, maintenance, and sharing of structured clinical-grade cancer mutations interpretations.
* **Where does the data comes from?** All interpretations written or approved by board-certificate molecular pathologists (PMKB's employees). All interpretations must be supported by at least 1 litterature citation
* **Other informations**  
    * Support of all major variant types: small localized mutations (SNV, indels, ...), copy number alterations and gene fusions
    * Distinct user roles including high-level approvers



## CIViC
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [CIViC](#civic)                                                       | 1936     | 358   | 08/08/18 | :white_check_mark: | :white_check_mark:      | 2017             | https://civicdb.org/home                     |

**Paper:** [link](https://www.nature.com/articles/ng.3774) Griffith M\*,†, Spies NC\*, Krysiak K\*, McMichael JF, Coffman AC, Danos AM, Ainscough BJ, Ramirez CA, Rieke DT, Kujan L, Barnell EK, Wagner AH, Skidmore ZL, Wollam A, Liu CJ, Jones MR, Bilski RL, Lesurf R, Feng YY, Shah NM, Bonakdar M, Trani L, Matlock M, Ramu A, Campbell KM, Spies GC, Graubert AP, Gangavarapu K, Eldred JM, Larson DE, Walker JR, Good BM, Wu C, Su AI, Dienstmann R, Margolin AA, Tamborero D, Lopez-Bigas N, Jones SJ, Bose R, Spencer DH Wartman LD, Wilson RK, Mardis ER, Griffith OL†. 2016. CIViC is a community knowledgebase for expert crowdsourcing the clinical interpretation of variants in cancer. Nat Genet. 49, 170–174 (2017); doi: http://dx.doi.org/10.1038/ng.3774. \*These authors contributed equally to this work. †Corresponding author.  

* **What is it?** CIViC is a community expert-crowdsourced knowledgebase for clinical interpretation of variants in cancer. It describes the therapeutic, prognostic, diagnosic and predisposing relevance of inherited and somatic variants of all types.
* **Where does the data comes from?** National team of experts collaborating remotely within a centralized curation interface. Agreement between at least two independant contributors (and at least one must be an expert editor) before acceptance of new evidence or revisions of existing content. Validated curators can add a variant description if there is evidence link to cancer with some clinical relevance.
* **Other informations**  
    * Scoring system of the variants.
    * Present itself as more open and transparent that the concurrency.
    * All variant types supported as well as all variants origine (somatic mutation, germline mutation and germline polymorphism).



## OncoKB
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [OncoKB](#oncokb)                                                     | 3971     | 477   | 09/08/18 | :white_check_mark: | -                       | 2017             | http://oncokb.org/#/                         |

**Paper:** [link](http://ascopubs.org/doi/full/10.1200/PO.17.00011) DOI: 10.1200/PO.17.00011 JCO Precision Oncology - published online May 16, 2017  

* **What is it?** Expert-guided precision oncology knowledge base. It annotates the biologic and oncongenic effects and prognostic and predictive significance of somatic molecular alterations.
* **Where does the data comes from?** Dedicated panel of physicians and cancer biologists who review and edit biomarker-associated investigational therapeutic strategis. "Continual dialogue with the scientific and medical community". Informtaions curated from multiple unstructured information resources including guidelines and recommendations from FDA labeling, NCCN guidelines, other disease-specific expert and advocacy group recommendations, and the medical literature. Panel of 22 MSK clinicians and physician scientists recognized as disease or gene experts in their field. 3.5 full time staff and 9 part-time curators (20h per week).
* **Other informations**  
    * More than 90% of alterations have curated biologic effects and are classified as oncogenic but are not associated with actionability.
    * Scoring system of clinical actionability.



## Personalized Cancer Therapy
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [Personalized Cancer Therapy](#personalized-cancer-therapy)           | ?        | ?     | -        | :x:                | :x:                     | 2017             | https://pct.mdanderson.org                   |

**Paper:** [link](http://cancerres.aacrjournals.org/content/77/21/e123.full-text.pdf) Katherine C. Kurnit, Ann M. Bailey, Jia Zeng, Amber M. Johnson, Md. Abu Shufean, Lauren Brusco, Beate C. Litzenburger, Nora S. Sánchez, Yekaterina B. Khotskaya, Vijaykumar Holla, Amy Simpson, Gordon B. Mills, John Mendelsohn, Elmer Bernstam, Kenna Shaw and Funda Meric-Bernstam “Personalized Cancer Therapy”: A Publicly Available Precision Oncology Resource Cancer Res November 1 2017 (77) (21) e123-e126; DOI: 10.1158/0008-5472.CAN-17-0341  

* **What is it?** Information on the function of common genomic alterations and their therapeutic implications. Clinical significance and actionability of genomic alterations and identification of matched targeted therapies.
* **Where does the data comes from?** High-throughput litterature from the MEDLINE database + manually reviewed litterature by a precision oncology decision support (team including oncologists, geneticists, molecular biologists, computational scientists, ...). They validate and record the functional implication in tumorigenesis of each alteration. Genes registered must 1) be cancer-associated, 2) have evidence that targeting the gene may result in tumor suppression, 3) drugs either FDA-approved or clinically investigated. Then a systematic scientific literrature review is performed. Functional annotation of variants: cBIO, COSMIC, published findings.
* **Other informations**
    * Comparison with OncoKB: clinical trials availables



## Cancer Genome Interpreter
| Database name                                                         | Variants | Genes | Date     | Public             | Results in the notebook | Publication date | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | :---------------------: | :--------------: | -------------------------------------------- |
| [Cancer Genome Interpreter](#cancer-genome-interpreter)               | 5601     | 765   | 08/08/18 | :white_check_mark: | :white_check_mark:      | 2018             | https://www.cancergenomeinterpreter.org/home |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5875005/) Tamborero D, Rubio-Perez C, Deu-Pons J, et al. Cancer Genome Interpreter annotates the biological and clinical relevance of tumor alterations. Genome Medicine. 2018;10:25. doi:10.1186/s13073-018-0531-8.  

* **What is it?** Cancer Genome Interpreter is a platform that systematizes the interpretation of cancer genomes, the main hallmark of which is streamlining and automatization of the whole process. It identifies all known and likely tumorigenic genomic alterations and annotate all variants that constitutes biomarkers.
* **Where does the data comes from?** Employs existing or newly developed resources and computational methods. Alterations that are clinically or experimentally validated to drive tumor phenotypes –previously culled from public sources– are identified by the CGI, whereas the effect of the remaining alterations of uncertain significance are predicted using in silico approaches, such as OncodriveMUT (for mutations). Validated oncogenic mutations catalog: DoCM, ClinVar and OncoKB + results of several published experimental assays.
* **Other informations**  
    * Automatically recognizes the format, remaps the variants as needed and standardized the annotation for downstream compatibility. 
    * All analysis are cancer-specific and thus the tumor type of the samples to analyze is required.
* **OncodriveMUT**  
    * The CGI asseses the tumorigenic potential of the variants of unknown significance with OncodriveMUT "a newly developed rule-based approach that combines the values of these features". Used by the CGI to analyze the mutations in cancer genes that are not found in the Catalog of Validated Oncogenic Mutations.
    * Relevant features used to classify the mutations:
        * Oncogene vs TSG
        * Consequence type (synonymous, missense, inframe indel or truncating)
        * Position within the transcript
        * If it falls in a mutation hotspot or cluster
        * Predicted functional impact
        * Frequency within the human population
        * If it occurs in a domain of the protein that is depleted of germline variants  
    * Using a set of heuristic rules. Compared the performance obtained with a machine-learning approach: random forest with 1,000 estimators trained in a ten fold cross-validation with 70% of the features in order to predict the remaining 30%. Both the machine-learning and the heuristic approach exhibited similar performace, therefore decided to use the heuristic rules.
    * Analyzed cohorts of tumors (6,792 samples across 28 cancer types) and samples from healthy donors (60,706 unrelated individuals).
    * Performance in the task of classifying driver and passenger mutations assessed using the Catalog of Validated Oncogenic Mutations (n = 5314) and a collected set of neutral PAMS affecting cancer gene (n = 1676): 86% accuracy.
