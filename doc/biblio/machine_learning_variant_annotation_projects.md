# Machine learning variant annotation projects

| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [CanPredict](#canpredict)             | 2007             | :x: (not available anymore)                            |
| [CHASM](#chasm)                       | 2009             | http://wiki.chasmsoftware.org/index.php/CHASM_Overview |
| [MutationAssessor](#mutationassessor) | 2011             | http://mutationassessor.org/r3/                        |
| [FATHMM](#fathmm)                     | 2013             | http://fathmm.biocompute.org.uk/index.html             |
| [CanDrA](#candra)                     | 2013             | http://bioinformatics.mdanderson.org/main/CanDrA       |
| [CScape](#cscape)                     | 2017             | http://cscape.biocompute.org.uk                        |
| [FATHMM-XF](#fathmm-xf)               | 2018             | http://fathmm.biocompute.org.uk/fathmm-xf/             |
| [rDriver](#rdriver)                   | 2018             | :x:                                                    |

*This is not an exhaustive list.*  

**Every algorithm works for nsSNVs only.**  

The following paper was used to complete the informations, we strongly recommend to read the part I. and II., that provide a complete overview of the topic before 2016.  
**Paper:** [link](https://onlinelibrary.wiley.com/doi/abs/10.1002/9780470015902.a0025331) Djotsa Nono, A. B., Chen, K. and Liu, X. (2016). Computational Prediction of Genetic Drivers in Cancer. In eLS, John Wiley & Sons, Ltd (Ed.). doi:10.1002/9780470015902.a0025331  



***



## CanPredict
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [CanPredict](#canpredict)             | 2007             | :x: (not available anymore)                            |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1933186/) Kaminker JS, Zhang Y, Watanabe C, Zhang Z. CanPredict: a computational tool for predicting cancer-associated missense mutations. Nucleic Acids Research. 2007;35(Web Server issue):W595-W598. doi:10.1093/nar/gkm405.  

* Algorithm: random forest
* Features: SIFT, Pfam-based LogR.E-value and GOSS
* Dataset:
	* 200 randomly selected known somatic cancer mutations from COSMIC database
	* 800 non-cancer, non-synonymous variants from dbSNP database (with minor allele frequency > 20%)
* Other: one of the first machine learning algorithm techniques designed especially to dicsriminate driver from passenger mutations in cancer



## CHASM
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [CHASM](#chasm)                       | 2009             | http://wiki.chasmsoftware.org/index.php/CHASM_Overview |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pubmed/19654296?ordinalpos=2&itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DefaultReportPanel.Pubmed_RVDocSum) Carter H, Chen S, Isik L, Tyekucheva S, Velculescu VE, Kinzler KW, Vogelstein B, Karchin R.(2009)Cancer-specific high-throughput annotation of somatic mutations: computational prediction of driver missense mutations.Cancer Research. 69(16):6660-7  

* Algorithm:
	* Random Forest (500 trees and default parameters mtry = 7)
	* Compared with SVM
	* Area under ROC curve > 0.91, area under precision-recall curve > 0.79
* Features:
	* 49 predictive features selected among 80 features
	* Feature selection: protocol based on mutual information (generalized version of correlation)
	* Features with missing values estimated with k-nearest neighbors algorithm
	* Prior to training all features standardized with the Z-score method
* Dataset:
	* 2488 missense driver mutations from COSMIC database and recent research: 1244 for feature selection and 1244 for classifier training
	* Synthetic passenger generated according to background base substitution frequencies observed for the specific tumor type (sampling from eight multinomial distributions that depend on di-nucleotide context and tumor type): 4500 for feature selection and 4500 for classifier training
* Other:
	* Last updated on the website on 2014
	* Propose a whole set of software and precomputed data to run CHASM on your own mutations dataset



## MutationAssessor
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [MutationAssessor](#mutationassessor) | 2011             | http://mutationassessor.org/r3/                        |

**Paper:** [link](https://academic.oup.com/nar/article/39/17/e118/2411278) Boris Reva, Yevgeniy Antipin, Chris Sander; Predicting the functional impact of protein mutations: application to cancer genomics, Nucleic Acids Research, Volume 39, Issue 17, 1 September 2011, Pages e118, https://doi.org/10.1093/nar/gkr407  

* Algorithm:
	* "Hypothesis: many mutations were tried in evolution in each sequence position sufficiently often such that the observed distributions of residues in aligned positions of homologous sequences reflect the functional constraints on these residues.", so possibility to convert the observed frequencies into a numerical estimate of the functional impact of a mutation
	* Specificity of 79%
* Dataset: UniProt
* Other:
	* It products a FIS (functional impact score) (like SIFT, PolyPhen-2, ...)
	* For any disease type
	* Applied to COSMIC database



## FATHMM
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [FATHMM](#fathmm)                     | 2013             | http://fathmm.biocompute.org.uk/index.html             |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pubmed/23033316) Shihab HA, Gough J, Cooper DN, et al. Predicting the Functional, Molecular, and Phenotypic Consequences of Amino Acid Substitutions using Hidden Markov Models. Human Mutation. 2013;34(1):57-65. doi:10.1002/humu.22225.  


* Algorithm:
	* Hidden Markov Models
	* Weighted/species-dependent or unweighted/species-independent
* Features: combines sequence-based conservation features (the alignement of homologous sequences and conserved protein domains) and pathogenicity weights (indicative of the overall tolerance of the protein model to mutations)
* Dataset: AAs = Amino Acid substitution
	* HGMD: 49,532 AAs
	* UniProt: 36,928 AAs
* Other:
	* Other article in May 2013 describing an adaptation to the FATHMM algorithm in which a cancer-specific weighting scheme was incorporated to potentiate the functional analysis of driver mutations (improved odds in identifying driver/passenger mutations using this weighting scheme)
	* Performed various existing and independent benchmarking:
		* VariBench: 40,740 AAs for an existing benchmarking
		* Hicks et al.2011: 267 AAs for an existing benchmarking
		* SwissVar: 59,976 AAs for  an independent benckmarking
	* Used in the COSMIC database to generate mutational impact scores



## CanDrA
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [CanDrA](#candra)                     | 2013             | http://bioinformatics.mdanderson.org/main/CanDrA       |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3813554/) Mao Y, Chen H, Liang H, Meric-Bernstam F, Mills GB, Chen K. CanDrA: Cancer-Specific Driver Missense Mutation Annotation with Optimized Features. Adamovic T, ed. PLoS ONE. 2013;8(10):e77945. doi:10.1371/journal.pone.0077945.  

* Algorithm:
	* Weighted SVM
	* 3 categories: driver, no-call and passenger
* Features:
	* 95 structural and evolutionary features computed by over 10 functional prediction algorithms (CHASM, SIFT, MutationAssessor, ENSEMBL, Variant Effect Predictor, MutationAssessor, ANNOVAR, PolyPhem-2, CONDEL, PhyloP, GERP++ and LRT)
	* See article for details on feature selection: 21 final features for GBM and 22 final features for OVC
	* Features with missing values estimated with k-nearest neighbors algorithm
* Dataset:
	* Driver mutation: mutation observed in at least two different samples, from either TCGA or COSMIC
	* 67 mutations for GBM and 61 for OVC (92.5% and 80.3% considered as drivers in previous study) only from COSMIC and TCGA
	* Passenger mutations from hyper-mutated samples (COSMIC, TCGA and CCLE): 490 mutations for GBM and 462 for OVC
	* Construction of a cancer-type specific expanded set of drivers and passengers following an empirical rule: 1529 GBM and 1768 OVC putative drivers, 1259 GBM and 8075 OVC passenger mutations.
		* Empirical rule: observed in at least 3 primary tumor samples (regardless of cancer type) OR site intersects at least 4 mutations (including indels, DNP or TNP) OR centered in a 25 bp region that intersects at least 5 mutations in the COSMIC database
		* Passenger mutations: absent within a 31bp window in COSMIC cancer census gene but seen only once in a primary tumor of a cancer types
* Other:
	* Work only on glioblastoma mutliforme (GBM) and ovarian carcinoma (OVC)
	* CanDrA Plus: 15 cancer types and extra model working for all cancer



## CScape
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [CScape](#cscape)                     | 2017             | http://cscape.biocompute.org.uk                        |

**Paper:** [link](https://www.nature.com/articles/s41598-017-11746-4) Rogers MF, Shihab H, Gaunt TR, Campbell C (2017). CScape: a tool for predicting oncogenic single-point mutations in the cancer genome. Nature Scientific Reports  

* Algorithm:
	* Multiple Kernel Learning
	* Leave-one-chromosome cross-validation, randomly selected balanced sets of 1,000 positive and 1,000 negative mutations
	* Two distinc classifiers: CS-coding for coding regions and CS-noncoding for noncoding regions
	* Balanced accuracy of 72.3% in coding regions and 62.9% in non-coding regions. Can achieve up to 91% balanced accuracy in coding regions and 70% in non-coding regions on independent dataset
* Features:
	* More than 30 features groups
	* New feature for the non-coding predictor
	* Greedy sequential learning to indentify an optimal combination og feature groups
* Dataset:
	* Positive 46,420 (pathogenic) dataset: COSMIC database (version 75, November 2015) with reccurence at least 5 for coding regions and 3 for non-coding regions (work done on finding the best threshold to increase accuracy while limiting bias)
	* Negative dataset: 131,714 SNVs from the 1,000 Genomes Project (could contain true positive because unannotated) located not too far from the positive dataset mutations
* Other:
	* Comparison with multiple algorithm
	* Tested on multiples databases (ICGC, TCGA, ClinVar, ...)



## FATHMM-XF
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [FATHMM-XF](#fathmm-xf)               | 2018             | http://fathmm.biocompute.org.uk/fathmm-xf/             |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5860356/) Rogers MF, Shihab HA, Mort M, Cooper DN, Gaunt TR, Campbell C. FATHMM-XF: accurate prediction of pathogenic point mutations via extended features. Hancock J, ed. Bioinformatics. 2018;34(3):511-513. doi:10.1093/bioinformatics/btx536.  

* Algorithm:
	* Supervised machine learning.
	* Non-coding regions: 92.3% accuracy (using 5 features groups)
	* Coding regions: 88% accuracy (using 6 features groups)
* Features:
	* 27 data sets (ENCODE, MIH Roadmap Epigenomics) + 4 additional features groups from conservation scores, the VEP, annotated gene models and the DNA sequence itself
	* Leave-one-chromosome-out-cross-validation
	* Platt scaling
* Dataset:
	* 156,775 positive example: HGMD
	* 25,720 neutral examples: the 1000 Genomes Project, only SNVs with a global minor VAF <= 1%, remove X and Y



## rDriver
| Methode name                          | Publication date | Website                                                |
| ------------------------------------- | :--------------: | ------------------------------------------------------ |
| [rDriver](#rdriver)                   | 2018             | :x:                                                    |

**Paper:** [link](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196939) Wang Z, Ng KS, Chen T, Kim TB, Wang F, et al. (2018) Cancer driver mutation prediction through Bayesian integration of multi-omic data. PLOS ONE 13(5): e0196939. https://doi.org/10.1371/journal.pone.0196939  

* Algorithm: Bayesian hierarchical modeling approach
* Features: Functional impact scores and genome-wide mRNA/protein expression levels
* Dataset: 3,080 tumor samples from 8 cancer types in the TCGA
* Other: Compared to other tools: more low frequency mutations 
