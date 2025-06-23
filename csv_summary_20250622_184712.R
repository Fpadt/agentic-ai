# CSV Summary Analysis using data.table
# File: padt\MD_PLANT.csv
# Generated: 2025-06-22 18:47:12
# Execute with: "C:\Program Files\R\R-4.5.0\bin\Rscript.exe" --vanilla csv_summary_20250622_184712.R

library(data.table)

# Load the CSV file
cat("Loading CSV file: padt\MD_PLANT.csv\n")
data <- fread("padt\MD_PLANT.csv")

cat("\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
cat("CSV SUMMARY REPORT FOR: MD_PLANT.csv\n")
cat(paste(rep("=", 60), collapse = ""), "\n\n")

# Basic dimensions
cat("BASIC INFORMATION:\n")
cat("- File path: padt\MD_PLANT.csv\n")
cat("- Number of rows: ", nrow(data), "\n")
cat("- Number of columns: ", ncol(data), "\n")
cat("- Total cells: ", nrow(data) * ncol(data), "\n")
cat("- File size (approx): ", file.size("padt\MD_PLANT.csv"), " bytes\n\n")

# Column names and types
cat("COLUMN INFORMATION:\n")
for(i in 1:ncol(data)) {
    col_name <- names(data)[i]
    col_class <- class(data[[i]])[1]
    cat(sprintf("- Column %d: %s (type: %s)\n", i, col_name, col_class))
}
cat("\n")

# Summary statistics for each column
cat("DETAILED COLUMN STATISTICS:\n")
cat(paste(rep("-", 40), collapse = ""), "\n")

for(col_name in names(data)) {
    cat("\nColumn:", col_name, "\n")
    
    # Basic stats
    cat("  - Data type:", class(data[[col_name]])[1], "\n")
    cat("  - Total values:", length(data[[col_name]]), "\n")
    cat("  - Missing values (NA):", sum(is.na(data[[col_name]])), "\n")
    cat("  - Non-missing values:", sum(!is.na(data[[col_name]])), "\n")
    cat("  - Unique values:", data[, uniqueN(get(col_name), na.rm = TRUE)], "\n")
    
    # For numeric columns
    if(is.numeric(data[[col_name]])) {
        if(sum(!is.na(data[[col_name]])) > 0) {
            stats <- data[, .(
                min_val = min(get(col_name), na.rm = TRUE),
                max_val = max(get(col_name), na.rm = TRUE),
                mean_val = mean(get(col_name), na.rm = TRUE),
                median_val = median(get(col_name), na.rm = TRUE),
                sd_val = sd(get(col_name), na.rm = TRUE)
            ), env = list(col_name = col_name)]
            
            cat("  - Minimum:", stats$min_val, "\n")
            cat("  - Maximum:", stats$max_val, "\n")
            cat("  - Mean:", round(stats$mean_val, 3), "\n")
            cat("  - Median:", stats$median_val, "\n")
            cat("  - Standard deviation:", round(stats$sd_val, 3), "\n")
        }
    }
    
    # For character/factor columns - show most frequent values
    if(is.character(data[[col_name]]) || is.factor(data[[col_name]])) {
        freq_table <- data[!is.na(get(col_name)), .N, by = col_name, env = list(col_name = col_name)]
        setorderv(freq_table, "N", order = -1)
        top_values <- head(freq_table, 5)
        
        if(nrow(top_values) > 0) {
            cat("  - Most frequent values:\n")
            for(i in 1:nrow(top_values)) {
                cat(sprintf("    %s: %d occurrences\n", 
                    top_values[[col_name]][i], top_values$N[i]))
            }
        }
    }
    
    cat("  ", paste(rep("-", 30), collapse = ""), "\n")
}

# Data quality assessment
cat("\nDATA QUALITY ASSESSMENT:\n")
cat(paste(rep("-", 30), collapse = ""), "\n")

# Missing data summary
total_cells <- nrow(data) * ncol(data)
total_missing <- sum(is.na(data))
missing_percentage <- round((total_missing / total_cells) * 100, 2)

cat("- Total missing values:", total_missing, "out of", total_cells, "cells\n")
cat("- Missing data percentage:", missing_percentage, "%\n")

# Columns with missing data
missing_summary <- data[, lapply(.SD, function(x) sum(is.na(x)))]
cols_with_missing <- names(missing_summary)[missing_summary > 0]

if(length(cols_with_missing) > 0) {
    cat("- Columns with missing data:\n")
    for(col in cols_with_missing) {
        missing_count <- missing_summary[[col]]
        missing_pct <- round((missing_count / nrow(data)) * 100, 2)
        cat(sprintf("  %s: %d missing (%s%%)\n", col, missing_count, missing_pct))
    }
} else {
    cat("- No missing data found!\n")
}

# Duplicate rows
duplicate_rows <- nrow(data) - data[, .N, by = names(data)][, .N]
cat("- Duplicate rows:", duplicate_rows, "\n")

# Summary table using data.table
cat("\nQUICK REFERENCE TABLE:\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

summary_dt <- data.table(
    Column = names(data),
    Type = sapply(data, function(x) class(x)[1]),
    Missing = sapply(data, function(x) sum(is.na(x))),
    Unique = sapply(names(data), function(col) data[, uniqueN(get(col), na.rm = TRUE)])
)
print(summary_dt)

cat("\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
cat("CSV SUMMARY ANALYSIS COMPLETE\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
