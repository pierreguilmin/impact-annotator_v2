# Please read the associated notebooks:
#     - analysis/compute_final_dataset/filter_and_process_raw_dataset.ipynb
#     - analysis/compute_final_dataset/annotate_final_dataset.ipynb


source("../utils/R/custom_tools.R")
setup_environment("../utils/R/")


##############################################
## get impact_annotated ######################
##############################################

id_colnames  <- c("ID_VARIANT",
                  "CHR",
                  "START",
                  "END",
                  "REF",
                  "ALT")

vep_colnames <- c("VEP_Consequence",
                  "VEP_SYMBOL",
                  "VEP_HGVSc",
                  "VEP_HGVSp",
                  "VEP_VARIANT_CLASS")

vep_add_colnames <- c("VEP_IMPACT",
                      "VEP_Existing_variation",
                      "VEP_CLIN_SIG",
                      "VEP_SIFT",
                      "VEP_PolyPhen",
                      "VEP_COSMIC_CNT")

vep_gnomad_colnames <- c("VEP_gnomAD_AF",
                         
                         "VEP_gnomAD_genome_AC.AN_AFR",
                         "VEP_gnomAD_genome_AC.AN_AMR",
                         "VEP_gnomAD_genome_AC.AN_ASJ",
                         "VEP_gnomAD_genome_AC.AN_EAS",
                         "VEP_gnomAD_genome_AC.AN_FIN",
                         "VEP_gnomAD_genome_AC.AN_NFE",
                         "VEP_gnomAD_genome_AC.AN_OTH",
                        
                         "VEP_gnomAD_exome_AC.AN_AFR",
                         "VEP_gnomAD_exome_AC.AN_AMR",
                         "VEP_gnomAD_exome_AC.AN_ASJ",
                         "VEP_gnomAD_exome_AC.AN_EAS",
                         "VEP_gnomAD_exome_AC.AN_FIN",
                         "VEP_gnomAD_exome_AC.AN_NFE",
                         "VEP_gnomAD_exome_AC.AN_OTH")

get_impact_annotated <- function() {
    impact_annotated <- read.table(paste0(data_folder_path, "/annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_20181105.txt"),
                                   sep = "\t", stringsAsFactors = FALSE, header = TRUE, comment = "#")

    impact_annotated <- impact_annotated[, c(id_colnames, vep_colnames, vep_add_colnames, vep_gnomad_colnames)]

    impact_vcf <- read.table(paste0(data_folder_path, "/annotate_with_click_annotvcf/all_IMPACT_mutations_20181105.vcf"),
                             sep = "\t", stringsAsFactors = FALSE, header = FALSE, comment = "#")
    colnames(impact_vcf) <- c("CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT")

    impact_vcf$OLD_REF <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][1])
    impact_vcf$OLD_ALT <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][2])
    impact_vcf$OLD_POS <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][3])

    impact_vcf$join_key <- paste(impact_vcf$CHROM, impact_vcf$POS, impact_vcf$REF, impact_vcf$ALT, sep = '_')

    impact_vcf <- unique(impact_vcf)
    impact_annotated <- unique(impact_annotated)

    impact_annotated <- left_join(impact_annotated, impact_vcf[, c("join_key", "OLD_REF", "OLD_ALT", "OLD_POS")], by = c("ID_VARIANT" = "join_key"))

    return (impact_annotated)
}


##############################################
## add click_annotvcf VEP annotations ########
##############################################

add_click_annotvcf_annotations <- function(impact, impact_annotated) {
    impact_annotated$join_key <- paste(impact_annotated$CHR,
                                       impact_annotated$OLD_POS,
                                       impact_annotated$OLD_REF,
                                       impact_annotated$OLD_ALT,
                                       sep = '_')

    impact$mut_key <- paste(impact$Chromosome,
                            impact$Start_Position,
                            impact$Reference_Allele,
                            impact$Tumor_Seq_Allele2,
                            sep = '_')

    colnames_to_keep <- c(vep_colnames, vep_add_colnames, vep_gnomad_colnames)

    impact <- left_join(impact, impact_annotated[, c("join_key", colnames_to_keep)], by = c("mut_key" = "join_key"))

    return (impact)
}


##############################################
## filter impact #############################
##############################################

is_overlapped_by_dnp_or_tnp <- function(data, tsb, chr, start) {
    result <- data %>% filter(Tumor_Sample_Barcode == tsb &
                              Chromosome == chr &
                              ((Variant_Type == "DNP" & (Start_Position == start | Start_Position == start - 1) |
                               (Variant_Type == "TNP" & (Start_Position == start | Start_Position == start - 1 | Start_Position == start - 2)))))

    if (nrow(result) == 0)
        return (FALSE)
    else
        return (TRUE)
}

filter_impact <- function(impact) {
    # [-7 features] remove the unique-value features
    impact[, c("Entrez_Gene_Id",
               "Center",
               "NCBI_Build",
               "Strand",
               "dbSNP_RS",
               "Matched_Norm_Sample_Barcode",
               "variant_status")] <- list(NULL)
    # [-3 features] remove the redundant features
    impact[, c("Match_Norm_Seq_Allele1", "Match_Norm_Seq_Allele2", "Tumor_Seq_Allele1")] <- list(NULL)


    # [~ every rows] select only the most deleterious VEP consequence
    impact$VEP_Consequence <- sapply(impact$VEP_Consequence, function(x) strsplit(x, '&')[[1]][1])
    # [-434,123 rows] keep only the coding and splicing VEP_Consequence mutations
    impact <- impact[impact$VEP_Consequence %in% c("missense_variant",
                                                   "frameshift_variant",
                                                   "stop_gained",
                                                   "splice_acceptor_variant",
                                                   "inframe_deletion",
                                                   "splice_donor_variant",
                                                   "inframe_insertion",
                                                   "start_lost",
                                                   "stop_lost"),]

    # [-7,552 rows] remove rows having `match_status = "Unmatched"` or `match_status = "Unknown"`
    impact <- impact[! impact$match_status %in% c("Unmatched", "Unknown"),]
    # [-1 features] remove the `match_status` feature
    impact$match_status <- NULL


    # [~642 rows] rename `confidence_class` in {"UNLIKELY_MERGED", "UNLIKELY_ARTIFACT", "UNLIKELY_NOISE", "UNLIKELY_IN_NORMAL"} to "UNLIKELY"
    impact$confidence_class[impact$confidence_class %in% c("UNLIKELY_MERGED", "UNLIKELY_ARTIFACT", "UNLIKELY_NOISE", "UNLIKELY_IN_NORMAL")] <- "UNLIKELY"
    # [-5,982 rows] remove rows having `confidence_class = UNKNOWN` or `confidence_class = OK_NOT_SO`
    impact <- impact[! impact$confidence_class %in% c("UNKNOWN", "OK_NOT_SO"),]


    # [-0 rows] remove the contaminated rows minor_contamination > 0.01
    impact <- impact[impact$minor_contamination <= 0.01,]
    # [-1 feature] remove the minor_contamination feature
    impact["minor_contamination"] <- NULL


    # [-372 rows] remove the rows having n_depth < 20
    impact <- impact[impact$n_depth >= 20,]


    # [-38 rows] remove the rows having t_alt_plus_count + t_alt_neg_count != t_alt_count
    impact <- impact[impact$t_alt_plus_count + impact$t_alt_neg_count == impact$t_alt_count,]


    # [-541 rows] remove the rows having t_alt_count = 0
    impact <- impact[impact$t_alt_count != 0,]


    # [+1 feature] create a sample mutation key feature to idenfity rows in a unique way
    impact$sample_mut_key <- paste(impact$Tumor_Sample_Barcode, impact$mut_key, sep = '_')
    # [+1 feature] create a patient key feature to idenfity unique patient
    impact$patient_key <- substr(impact$Tumor_Sample_Barcode, 1, 9)


    # [-823 rows] remove the rows having Hugo_Symbol = CDKN2Ap14ARF and CDKN2Ap16INK4A in the tumor sample
    dd <- impact %>% group_by(Tumor_Sample_Barcode) %>%
                     summarise(has_both_reading_frame = ("CDKN2Ap14ARF" %in% Hugo_Symbol & "CDKN2Ap16INK4A" %in% Hugo_Symbol)) %>%
                     filter(has_both_reading_frame)
    impact <- impact[! (impact$Hugo_Symbol == "CDKN2Ap14ARF" & impact$Tumor_Sample_Barcode %in% dd$Tumor_Sample_Barcode),]


    # [-38 rows] duplicated mutation for the same sample_mut_key
    impact_redundant_to_delete <- impact %>% group_by(sample_mut_key) %>%
                                             filter(n() >= 2) %>%
                                             filter(t_depth == min(t_depth)) %>%
                                             filter(t_vaf == min(t_vaf))
    impact <- impact[! (impact$sample_mut_key %in% impact_redundant_to_delete$sample_mut_key &
                        impact$t_depth %in% impact_redundant_to_delete$t_depth &
                        impact$t_vaf %in% impact_redundant_to_delete$t_vaf),]


    # [-3,841 rows] SNV found as DNP or TNP
    overlapping_risk_dnp_or_tnp <- as.data.frame(impact %>% group_by(Tumor_Sample_Barcode, VEP_SYMBOL) %>%
                                                            filter(n() > 1 &
                                                                   "SNP" %in% Variant_Type &
                                                                   ("DNP" %in% Variant_Type |
                                                                    "TNP" %in% Variant_Type)))
    overlapping_dnp_or_tnp <- overlapping_risk_dnp_or_tnp %>% filter(Variant_Type == "SNP") %>%
                                                              group_by(sample_mut_key) %>%
                                                              filter(is_overlapped_by_dnp_or_tnp(overlapping_risk_dnp_or_tnp, Tumor_Sample_Barcode, Chromosome, Start_Position)) %>%
                                                              select(sample_mut_key)
    impact <- impact[! impact$sample_mut_key %in% overlapping_dnp_or_tnp$sample_mut_key,]


    return (impact)
}


##############################################
## process raw features ######################
##############################################

replace_na <- function(data, feature_name, replace_value){
    data[is.na(data[,feature_name]), feature_name] <- replace_value
    
    return (data)
}

get_HGVSp_from_vep <- function(HGVSp_string) {
    
    if (HGVSp_string == "unknown")
        return ("unknown")
    
    HGVSp_string <- strsplit(HGVSp_string, ':')[[1]][2]
    
    protein_long_name <- c('Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Glu', 'Gln', 'Gly', 'His', 'Ile', 'Leu', 'Lys',
                           'Met', 'Phe', 'Pro', 'Ser', 'Thr', 'Trp', 'Tyr', 'Val')
    protein_short_name <- c('A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K',
                            'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V')
    
    for (name in protein_long_name)
        HGVSp_string <- gsub(name, protein_short_name[match(name, protein_long_name)], HGVSp_string)
    
    HGVSp_string <- gsub('Ter', '*', HGVSp_string)
    HGVSp_string <- gsub('%3D', '=', HGVSp_string)
    
    return (HGVSp_string)
}

get_cosmic_count_from_vep <- function(cosmic_count_string) {
    if (cosmic_count_string == "unknown")
        return (0)
    else
        return (sum(as.numeric(strsplit(cosmic_count_string, '&')[[1]])))
}

get_simplified_clin_sig <- function(clin_sig_string) {
    if (clin_sig_string == "unknown")
        return ("unknown")
    else {
        tags <- unique(strsplit(clin_sig_string, '&')[[1]])
        
        tags <- gsub('likely_pathogenic', 'pathogenic', tags)
        tags <- gsub('drug_response'    , 'pathogenic', tags)
        tags <- gsub('risk_factor'      , 'pathogenic', tags)
        tags <- gsub('likely_benign'    , 'benign'    , tags)
        
        tags <- unique(tags)

        tags <- tags[! tags %in% c("not_provided", "uncertain_significance", "other")]
        
        if (length(tags) == 0 || length(tags) > 1)
            return ("unknown")
        else
            return (tags)
    }
}

get_gnomAD_total_AC.AN_pop <- function(data, pop_name) {
    genome_AC = as.integer(strsplit(data[paste0("VEP_gnomAD_genome_AC.AN_", pop_name)], ' \\| ')[[1]][1])
    genome_AN = as.integer(strsplit(data[paste0("VEP_gnomAD_genome_AC.AN_", pop_name)], ' \\| ')[[1]][2])

    exome_AC = as.integer(strsplit(data[paste0("VEP_gnomAD_exome_AC.AN_", pop_name)], ' \\| ')[[1]][1])
    exome_AN = as.integer(strsplit(data[paste0("VEP_gnomAD_exome_AC.AN_", pop_name)], ' \\| ')[[1]][2])
    
    return (paste(genome_AC + exome_AC, genome_AN + exome_AN, sep = ' | '))
}

get_gnomAD_total_AF_pop <- function(data, pop_name) {
        
    AC = as.integer(strsplit(data[paste0("VEP_gnomAD_total_AC.AN_", pop_name)], ' \\| ')[[1]][1])
    AN = as.integer(strsplit(data[paste0("VEP_gnomAD_total_AC.AN_", pop_name)], ' \\| ')[[1]][2])
    
    if (AN == 0)
        return (0)
    else
        return (AC / AN)
}

get_gnomAD_total_AF <- function(data) {
    
    AC <- c()
    AN <- c()
    
    for (pop in c('AFR', 'AMR', 'ASJ', 'EAS', 'FIN', 'NFE', 'OTH')) {
        AC <- c(AC, as.integer(strsplit(data[paste0("VEP_gnomAD_total_AC.AN_", pop)], ' \\| ')[[1]][1]))
        AN <- c(AN, as.integer(strsplit(data[paste0("VEP_gnomAD_total_AC.AN_", pop)], ' \\| ')[[1]][2]))
    }
                
    if (sum(AN) == 0)
        return (0)
    else
        return (sum(AC) / sum(AN))
}

process_raw_features <- function(impact) {
    # [~ every rows] NA -> "unknown"
    impact <- replace_na(impact, "VEP_HGVSc"             , "unknown")
    impact <- replace_na(impact, "VEP_HGVSp"             , "unknown")
    impact <- replace_na(impact, "VEP_Existing_variation", "unknown")
    impact <- replace_na(impact, "VEP_CLIN_SIG"          , "unknown")
    impact <- replace_na(impact, "VEP_SIFT"              , "unknown")
    impact <- replace_na(impact, "VEP_PolyPhen"          , "unknown")
    impact <- replace_na(impact, "VEP_COSMIC_CNT"        , "unknown")
    

    # [~ every rows] NA -> 0.0
    impact <- replace_na(impact, "VEP_gnomAD_AF", 0.0)
    # [~ every rows] NA -> "0 | 0"
    for (c in vep_gnomad_colnames[grepl("_AC.AN_", vep_gnomad_colnames)])
        impact <- replace_na(impact, c, " 0 | 0")


    # [~ every rows] occurence_in_normals -> frequency_in_normals
    impact$occurence_in_normals[impact$occurence_in_normals == '0'] <- "0;0"
    impact$occurence_in_normals[!grepl(';', impact$occurence_in_normals)] <- paste('0;', impact$occurence_in_normals[!grepl(';', impact$occurence_in_normals)])
    impact$frequency_in_normals <- sapply(impact$occurence_in_normals,
                                          function(s) as.double(strsplit(s, split = ';')[[1]][2]))
    impact$occurence_in_normals <- NULL


    # [~ every rows] VEP_HGVSc -> readable VEP_HGVSc
    impact$VEP_HGVSc <- sapply(impact$VEP_HGVSc, function(x) strsplit(x, ':')[[1]][2])
    impact <- replace_na(impact, "VEP_HGVSc", "unknown") # 5 NA values that we need to handle


    # [~ every rows] VEP_HGVSp -> readable VEP_HGVSp
    impact$VEP_HGVSp <- sapply(impact$VEP_HGVSp, get_HGVSp_from_vep)


    # [~ every rows] VEP_SIFT -> VEP_SIFT_class & VEP_SIFT_score
    impact$VEP_SIFT_class <- sapply(impact$VEP_SIFT, function(x) strsplit(x, '\\(')[[1]][1])
    impact$VEP_SIFT_score <- sapply(impact$VEP_SIFT, function(x) as.numeric(gsub(')', '', strsplit(x, '\\(')[[1]][2])))
    impact$VEP_SIFT <- NULL


    # [~ every rows] VEP_PolyPhen -> VEP_PolyPhen_class & VEP_PolyPhen_score
    impact$VEP_PolyPhen_class <- sapply(impact$VEP_PolyPhen, function(x) strsplit(x, '\\(')[[1]][1])
    impact$VEP_PolyPhen_score <- sapply(impact$VEP_PolyPhen, function(x) as.numeric(gsub(')', '', strsplit(x, '\\(')[[1]][2])))
    impact$VEP_PolyPhen <- NULL


    # [~ every rows] VEP_Existing_variation -> VEP_in_dbSNP
    impact$VEP_in_dbSNP <- grepl("rs", impact$VEP_Existing_variation)
    impact$VEP_Existing_variation <- NULL


    # [~ every rows] VEP_COSMIC_CNT -> readable VEP_COSMIC_CNT
    impact$VEP_COSMIC_CNT <- sapply(impact$VEP_COSMIC_CNT, get_cosmic_count_from_vep)


    # [~ every rows] VEP_CLIN_SIG -> readable VEP_CLIN_SIG
    impact$VEP_CLIN_SIG <- sapply(impact$VEP_CLIN_SIG, get_simplified_clin_sig)


    # [+7 features] VEP_gnomAD_total_AC.AN_<POP> (temporary feature)
    for (pop in c('AFR', 'AMR', 'ASJ', 'EAS', 'FIN', 'NFE', 'OTH'))
        impact[, paste0("VEP_gnomAD_total_AC.AN_", pop)] <- apply(impact, 1, function(x) get_gnomAD_total_AC.AN_pop(x, pop))
    # [+7 features] VEP_gnomAD_total_AF_<POP>
    for (pop in c('AFR', 'AMR', 'ASJ', 'EAS', 'FIN', 'NFE', 'OTH'))
        impact[, paste0("VEP_gnomAD_total_AF_", pop)] <- apply(impact, 1, function(x) get_gnomAD_total_AF_pop(x, pop))
    # [+1 feature] VEP_gnomAD_total_AF_max
    total_AF_columns <- colnames(impact)[grepl("VEP_gnomAD_total_AF_", colnames(impact))]
    impact$VEP_gnomAD_total_AF_max <- apply(impact, 1, function(x) max(as.numeric(x[total_AF_columns])))
    # [+1 feature] VEP_gnomAD_total_AF
    impact$VEP_gnomAD_total_AF <- apply(impact, 1, get_gnomAD_total_AF)
    # [-21 features] remove VEP_gnomAD_genome_AC.AN_<POP>, VEP_gnomAD_exome_AC.AN_<POP> and VEP_gnomAD_total_AC.AN_<POP>
    impact <- impact[, colnames(impact)[! (grepl("VEP_gnomAD_genome_AC.AN", colnames(impact)) |
                                           grepl("VEP_gnomAD_exome_AC.AN", colnames(impact)) |
                                           grepl("VEP_gnomAD_total_AC.AN", colnames(impact)))]]


    # [~ every rows] variant_caller_cv -> readable variant_caller_cv
    variant_caller_table <- c("MUTECT_ANNOVAR",
                              "SOMATICINDEL_ANNOVAR",
                              "PINDEL_ANNOVAR",
                              "SID_PINDEL_ANNOVAR",
                              "UNKNOWN",
                              "HTC",
                              "MutectHTC",
                              "MUTECT_VARDICT",
                              "PINDEL_VARDICT",
                              "SID_PINDEL_VARDICT",
                              "SID_VARDICT",
                              "VARDICT")
    impact$variant_caller_cv <- sapply(impact$variant_caller_cv, function(x) variant_caller_table[x])


    return (impact)
}


# #######################################
# ## get final dataset ##################
# #######################################

get_final_dataset <- function() {
    cat("Get raw impact...")
    impact <- read.table(paste0(data_folder_path, "/raw/all_IMPACT_mutations_20181105.txt"),
                         sep = "\t", stringsAsFactors = FALSE, header = TRUE)
    cat(" done!\n")

    cat("Get impact_annotated (impact annotated with click_annotvcf)...")
    impact_annotated <- get_impact_annotated()
    cat(" done!\n")

    cat("Join impact and impact_annotated...")
    impact <- add_click_annotvcf_annotations(impact, impact_annotated)
    cat(" done!\n")

    cat("Filter impact...")
    impact <- filter_impact(impact)
    cat(" done!\n")

    cat("Process raw features...")
    impact <- process_raw_features(impact)
    cat(" done!\n")

    write.table(impact, paste0(data_folder_path, "/processed/final_IMPACT_mutations_20181105.txt"), sep = "\t", row.names = FALSE)
}


##############################################
## add new features ##########################
##############################################

add_new_features <- function(impact) {

    # ## OncoKB ######################################
    # 1. Get the raw data
    impact_oncokb <- read.table(paste0(data_folder_path, "/annotate_with_oncokb/oncokb_annotated_final_IMPACT_mutations_20181105.txt"),
                                sep = "\t", stringsAsFactors = FALSE, header = TRUE)

    # 2. Create keys to join the two dataframes and extract the features
    impact_oncokb <- unique(impact_oncokb[, c("mut_key", "is.a.hotspot", "is.a.3d.hotspot", "oncogenic")])
    impact <- left_join(impact, impact_oncokb[, c("mut_key", "is.a.hotspot", "is.a.3d.hotspot", "oncogenic")], by = c("mut_key" = "mut_key"))

    # 3. Process the raw features
    ## is_a_hostpot
    colnames(impact)[colnames(impact) == "is.a.hotspot"] <- "is_a_hotspot"
    impact$is_a_hotspot[impact$is_a_hotspot == "Y"  ] <- "yes"
    impact$is_a_hotspot[impact$is_a_hotspot != "yes"] <- "unknown"

    ## is_a_3d_hostpot
    colnames(impact)[colnames(impact) == "is.a.3d.hotspot"] <- "is_a_3d_hotspot"
    impact$is_a_3d_hotspot[impact$is_a_3d_hotspot == "Y"  ] <- "yes"
    impact$is_a_3d_hotspot[impact$is_a_3d_hotspot != "yes"] <- "unknown"

    ## oncogenic
    impact$oncogenic[impact$oncogenic == ""] <- "Unknown"


    # ## gene_type #####################################
    # 1. Get the raw data
    cancer_genes_list <- read.table(paste0(data_folder_path, "/other_databases/CancerGenesList.txt"),
                                      sep = "\t", stringsAsFactors = FALSE, header = TRUE, comment.char = '')

    # 2. Create keys to join the two dataframes and extract the features
    impact <- left_join(impact, cancer_genes_list[, c("Hugo.Symbol", "OncoKB.Oncogene", "OncoKB.TSG")], by = c("VEP_SYMBOL" = "Hugo.Symbol"))

    # 3. Process the raw features
    ## gene_type
    impact$gene_type <- "unknown"
    impact$gene_type[impact$OncoKB.Oncogene == "Yes"] <- "oncogene"
    impact$gene_type[impact$OncoKB.TSG == "Yes"]      <- "tsg"
    impact$gene_type[impact$OncoKB.Oncogene == "Yes" & impact$OncoKB.TSG == "Yes"] <- "oncogene_and_tsg"

    impact$OncoKB.Oncogene <- NULL
    impact$OncoKB.TSG      <- NULL


    return (impact)
}


# #######################################
# ## annotate final dataset #############
# #######################################

annotate_final_dataset <- function() {
    cat("Get final impact...")
    impact <- read.table(paste0(data_folder_path, "/processed/final_IMPACT_mutations_20181105.txt"),
                         sep = "\t", stringsAsFactors = FALSE, header = TRUE)
    cat(" done!\n")

    cat("Add new features...")
    impact <- add_new_features(impact)
    cat(" done!\n")

    write.table(impact, paste0(data_folder_path, "/processed/annotated_final_IMPACT_mutations_20181105.txt"), sep = "\t", row.names = FALSE)
}
