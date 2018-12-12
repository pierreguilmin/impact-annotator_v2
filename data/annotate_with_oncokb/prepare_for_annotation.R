impact <- read.table("../processed/final_IMPACT_mutations_20181105.txt",
					 sep = "\t", stringsAsFactors = FALSE, header = TRUE)


impact <- impact[,c("mut_key", "VEP_SYMBOL", "VEP_Consequence", "VEP_VARIANT_CLASS", "VEP_HGVSp")]

colnames(impact) <- c("mut_key", "Hugo_Symbol", "VEP_Consequence", "VEP_VARIANT_CLASS", "HGVSp_Short")


selected_mutation_types = c("missense_variant",
                            "frameshift_variant",
                            "stop_gained",
                            "splice_acceptor_variant",
                            "inframe_deletion",
                            "splice_donor_variant",
                            "inframe_insertion",
                            "start_lost",
                            "stop_lost")

get_variant_classification <- function(data) {
    if (data["VEP_Consequence"] == "frameshift_variant") {
        if (data["VEP_VARIANT_CLASS"] == "insertion")
            return ("Frame_Shift_Ins")
        else
            return ("Frame_Shift_Del")
    }
    

    Variant_Classification = c("Missense_Mutation", 
                               "-",
                               "Nonsense_Mutation",
                               "Splice_Site",
                               "In_Frame_Del",
                               "Splice_Site",
                               "In_Frame_Ins",
                               "Start_Codon_Del",
                               "Nonstop_Mutation")
    
    return (Variant_Classification[match(data["VEP_Consequence"], selected_mutation_types)])
}

impact$Variant_Classification <- apply(impact, 1, get_variant_classification)

impact <- unique(impact)

write.table(impact, "ready_to_annotate_final_IMPACT_mutations_20181105.txt", sep = "\t", row.names = FALSE)
