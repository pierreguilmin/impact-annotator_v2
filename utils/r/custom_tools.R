##############################################
## custom R tools ############################
##############################################

# setup the environnment by loading the appropriate libraries and scripts
setup_environment <- function(utils_folder_name) {

  source(paste0(utils_folder_name, "/custom_tools_ggplot.R")) # ggplot tools

  suppressPackageStartupMessages(library("tidyverse"))
  suppressPackageStartupMessages(library("gridExtra")) # used to arrange ggplots in a grid

  theme_set(theme_minimal())

  options(repr.plot.res = 300,        # set a high-definition resolution for the jupyter notebooks plots (DPI)
          repr.matrix.max.rows = 600, # set the maximum number of rows displayed
          repr.matrix.max.cols = 200) # set the maximum number of columns displayed
}


# print the count and proportion of the numerator over the denominator, output example: "63603 over 248350 (25.61%)"
# the d_specifier and f_specifier parameters permits to align printing if the function is used in a for loop
print_count_and_proportion <- function(numerator, denominator, d_specifier = NULL, f_specifier = NULL) {

  if (missing(d_specifier))
    sprintf_string <- "%d over %d"
  else
    sprintf_string <- paste0("%", d_specifier, "d over %", d_specifier, "d")

  if (missing(f_specifier))
    sprintf_string <- paste0(sprintf_string, " (%.2f%%)")
  else
    sprintf_string <- paste0(sprintf_string, paste0(" (%", f_specifier, ".2f%%)"))

  sprintf(sprintf_string, numerator, denominator, 100 * numerator / denominator)
}


# print the size of a dataframe
print_size <- function(data) {
    cat(sprintf("Size of %s: %d x %d", deparse(substitute(data)), nrow(data), ncol(data)))
}


# print a custom sorted table of a categorical feature (with count and frequency)
get_table <- function(data, sum = TRUE, remove_null_values = FALSE) {
    count_table <- rev(sort(table(data)))

    prop_table  <- round(prop.table(count_table) * 100, 1)
    
    summary <- data.frame(names(count_table),
                          as.vector(count_table),
                          paste0(as.character(prop_table), "%"))
    
    colnames(summary) <- c("values", "count", "freq")
    
    if (remove_null_values)
    	summary <- summary[summary$count > 0,]

    if (sum)
        summary <- rbind(summary, data.frame("values" = "-- total --", "count" = length(data), "freq" = "100%"))

    return (summary)
}


get_simple_table <- function(data, sum = TRUE, min) {
    
    table <- rev(sort(table(data)))
        
    if (! missing(min))
        table <- table[as.vector(table >= min)]
        
    if (sum)
        table <- addmargins(table)
    
    return (table)
}
