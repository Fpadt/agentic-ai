# dev_assistant.py
from mcp.server.fastmcp import FastMCP
import os
import time

mcp = FastMCP("R Python Development Assistant")

# =============================================================================
# PYTHON EXECUTION TOOLS
# =============================================================================

@mcp.tool()
def run_python_code(code: str) -> str:
    """Execute Python code and return the output"""
    try:
        import io
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        # Execute code
        exec(code)
        
        # Get output
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        return f"Python Output:\n{output}" if output else "Code executed successfully (no output)"
        
    except Exception as e:
        return f"Python Error:\n{str(e)}"

# =============================================================================
# CSV ANALYSIS TOOLS (IMMEDIATE RESULTS)
# =============================================================================

@mcp.tool()
def polars_csv_analysis(file_path: str, separator: str = ';') -> str:
    """Fast and comprehensive CSV analysis using Polars (best for European data)"""
    try:
        import polars as pl
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        # Read with polars (handles semicolons well)
        df = pl.read_csv(file_path, separator=separator)
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        result = []
        result.append("⚡ POLARS CSV ANALYSIS")
        result.append("=" * 40)
        result.append(f"📄 File: {file_name}")
        result.append(f"📏 Size: {file_size:,} bytes")
        result.append(f"🔧 Separator: '{separator}'")
        result.append(f"📊 Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
        result.append("")
        
        # Column structure
        result.append("🏗️  COLUMN STRUCTURE:")
        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].null_count()
            unique_count = df[col].n_unique()
            null_pct = (null_count / df.shape[0]) * 100
            
            result.append(f"  {col:<20} | {dtype:<12} | {null_count:>2} missing ({null_pct:>4.1f}%) | {unique_count:>3} unique")
        
        result.append("")
        
        # Show complete data for small datasets
        if df.shape[0] <= 25:
            result.append("📋 COMPLETE DATASET:")
            result.append(str(df))
        else:
            result.append("👀 SAMPLE DATA (first 10 rows):")
            result.append(str(df.head(10)))
        
        result.append("")
        
        # Data quality summary
        total_cells = df.shape[0] * df.shape[1]
        total_nulls = sum(df[col].null_count() for col in df.columns)
        completeness = ((total_cells - total_nulls) / total_cells) * 100
        duplicates = df.shape[0] - df.unique().shape[0]
        
        result.append("🔍 DATA QUALITY:")
        result.append(f"  Completeness: {completeness:.2f}%")
        result.append(f"  Missing cells: {total_nulls}/{total_cells}")
        result.append(f"  Duplicate rows: {duplicates}")
        
        result.append("")
        result.append("✅ Analysis complete - Polars handles European CSV formats perfectly!")
        
        return "\n".join(result)
        
    except ImportError:
        return """❌ POLARS NOT INSTALLED
        
To install: pip install polars

Polars is recommended for:
- Faster CSV processing
- Better European format support
- No timeout issues"""
        
    except Exception as e:
        return f"❌ Polars error: {str(e)}"


@mcp.tool()
def pandas_csv_analysis(file_path: str, separator: str = ';') -> str:
    """CSV analysis using pandas (fallback if Polars unavailable)"""
    try:
        import pandas as pd
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        df = pd.read_csv(file_path, sep=separator)
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        result = []
        result.append("📊 PANDAS CSV ANALYSIS")
        result.append("=" * 35)
        result.append(f"📄 File: {file_name}")
        result.append(f"📏 Size: {file_size:,} bytes")
        result.append(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        result.append("")
        
        # Column info
        result.append("📋 COLUMNS:")
        for i, col in enumerate(df.columns, 1):
            dtype = str(df[col].dtype)
            missing = df[col].isna().sum()
            unique = df[col].nunique()
            result.append(f"  {i:2d}. {col:<20} | {dtype:<10} | {missing:>2} missing | {unique:>3} unique")
        result.append("")
        
        # Show data
        if df.shape[0] <= 20:
            result.append("📝 ALL DATA:")
            data_str = df.to_string(index=False)
            for line in data_str.split('\n'):
                result.append(f"  {line}")
        else:
            result.append("👀 SAMPLE DATA:")
            sample_str = df.head(10).to_string(index=False)
            for line in sample_str.split('\n'):
                result.append(f"  {line}")
        
        result.append("")
        
        # Data quality
        total_missing = df.isna().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        duplicates = df.duplicated().sum()
        
        result.append("🔍 DATA QUALITY:")
        result.append(f"  Missing values: {total_missing}/{total_cells} ({(total_missing/total_cells)*100:.1f}%)")
        result.append(f"  Duplicate rows: {duplicates}")
        
        result.append("")
        result.append("✅ Pandas analysis complete")
        
        return "\n".join(result)
        
    except ImportError:
        return "❌ Pandas not installed. Try: pip install pandas"
    except Exception as e:
        return f"❌ Pandas error: {str(e)}"


@mcp.tool()
def quick_csv_peek(file_path: str) -> str:
    """Ultra-fast CSV preview without any external libraries"""
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        # Minimal file reading
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [f.readline().strip() for _ in range(5)]
        
        size = os.path.getsize(file_path)
        sep = ';' if ';' in lines[0] else ','
        
        result = []
        result.append("📄 QUICK CSV PEEK")
        result.append("=" * 25)
        result.append(f"File: {os.path.basename(file_path)} ({size:,} bytes)")
        result.append(f"Separator: '{sep}'")
        result.append("")
        
        for i, line in enumerate(lines):
            if line:
                cols = line.split(sep)
                result.append(f"Row {i+1}: {cols}")
        
        result.append("")
        result.append("✅ Ultra-fast preview complete")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# =============================================================================
# R SCRIPT GENERATION TOOLS
# =============================================================================

@mcp.tool()
def create_r_script(code: str, script_name: str = "analysis") -> str:
    """Create an R script file for manual execution"""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{script_name}_{timestamp}.R"
        
        r_content = f"""# MCP Generated R Script: {script_name}
# Created: {time.strftime("%Y-%m-%d %H:%M:%S")}
# Execute with: "C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe" --vanilla {filename}

{code}

# End of script
"""
        
        with open(filename, "w") as f:
            f.write(r_content)
        
        return f"""✅ R script created: {filename}

To execute:
"C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe" --vanilla {filename}

Location: {os.getcwd()}\\{filename}
"""
        
    except Exception as e:
        return f"❌ Error creating R script: {str(e)}"


@mcp.tool()
def create_comprehensive_csv_r_script(file_path: str) -> str:
    """Create comprehensive R script for CSV analysis using data.table"""
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found at {file_path}"
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        script_name = f"csv_analysis_{timestamp}.R"
        file_name = os.path.basename(file_path)
        
        r_content = f'''# Comprehensive CSV Analysis using data.table
# File: {file_path}
# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

# Install and load required packages
if (!require(data.table)) {{
    install.packages("data.table")
    library(data.table)
}}

# Load the CSV file (data.table automatically detects separators)
cat("Loading CSV file: {file_name}\\n")
data <- fread("{file_path}")

cat("\\n")
cat(paste(rep("=", 70), collapse = ""), "\\n")
cat("COMPREHENSIVE CSV ANALYSIS REPORT\\n")
cat("File: {file_name}\\n")
cat("Generated:", Sys.time(), "\\n")
cat(paste(rep("=", 70), collapse = ""), "\\n\\n")

# Basic information
cat("📊 BASIC INFORMATION:\\n")
cat("   Rows:", format(nrow(data), big.mark=","), "\\n")
cat("   Columns:", ncol(data), "\\n")
cat("   Total cells:", format(nrow(data) * ncol(data), big.mark=","), "\\n\\n")

# Column overview
cat("📋 COLUMN OVERVIEW:\\n")
for(i in 1:ncol(data)) {{
    col_name <- names(data)[i]
    col_class <- class(data[[i]])[1]
    missing_count <- sum(is.na(data[[i]]))
    unique_count <- data[, uniqueN(get(col_name), na.rm = TRUE)]
    
    cat(sprintf("   %2d. %-20s | %-10s | %6s missing | %6s unique\\n", 
               i, col_name, col_class, format(missing_count, big.mark=","), 
               format(unique_count, big.mark=",")))
}}

# Show complete data for small datasets
if(nrow(data) <= 50) {{
    cat("\\n📋 COMPLETE DATASET:\\n")
    print(data)
}} else {{
    cat("\\n👀 FIRST 10 ROWS:\\n")
    print(head(data, 10))
    cat("\\n👀 LAST 5 ROWS:\\n")
    print(tail(data, 5))
}}

# Detailed column analysis
cat("\\n🔍 DETAILED COLUMN ANALYSIS:\\n")
cat(paste(rep("-", 50), collapse = ""), "\\n")

for(col_name in names(data)) {{
    cat("\\n📈 Column:", col_name, "\\n")
    
    col_data <- data[[col_name]]
    total_vals <- length(col_data)
    missing_vals <- sum(is.na(col_data))
    non_missing <- total_vals - missing_vals
    
    cat("   Type:", class(col_data)[1], "\\n")
    cat("   Missing:", missing_vals, "/", total_vals, 
        sprintf("(%.1f%%)\\n", (missing_vals/total_vals)*100))
    cat("   Unique values:", data[, uniqueN(get(col_name), na.rm = TRUE)], "\\n")
    
    if(is.numeric(col_data) && non_missing > 0) {{
        # Numeric statistics
        stats_data <- col_data[!is.na(col_data)]
        cat("   📊 Numeric Statistics:\\n")
        cat("      Min:", min(stats_data), "\\n")
        cat("      Max:", max(stats_data), "\\n")
        cat("      Mean:", round(mean(stats_data), 3), "\\n")
        cat("      Median:", median(stats_data), "\\n")
        cat("      Std Dev:", round(sd(stats_data), 3), "\\n")
        
        # Quartiles
        quartiles <- quantile(stats_data, probs = c(0.25, 0.75))
        cat("      Q1:", quartiles[1], " | Q3:", quartiles[2], "\\n")
        
    }} else if((is.character(col_data) || is.factor(col_data)) && non_missing > 0) {{
        # Categorical statistics
        freq_table <- data[!is.na(get(col_name)), .N, by = col_name, env = list(col_name = col_name)]
        setorderv(freq_table, "N", order = -1)
        top_values <- head(freq_table, 5)
        
        cat("   📝 Top Values:\\n")
        for(i in 1:min(nrow(top_values), 5)) {{
            value <- top_values[[col_name]][i]
            count <- top_values$N[i]
            pct <- round((count / non_missing) * 100, 1)
            cat(sprintf("      %s: %s (%s%%)\\n", value, count, pct))
        }}
    }}
    
    cat("   ", paste(rep("-", 40), collapse = ""), "\\n")
}}

# Data quality assessment
cat("\\n🔍 DATA QUALITY ASSESSMENT:\\n")
cat(paste(rep("-", 40), collapse = ""), "\\n")

total_cells <- nrow(data) * ncol(data)
total_missing <- sum(is.na(data))

cat("Missing data overview:\\n")
cat("   Total missing values:", format(total_missing, big.mark=","), "\\n")
cat("   Percentage missing:", round((total_missing/total_cells)*100, 2), "%\\n")

# Check for duplicates
duplicate_count <- nrow(data) - data[, .N, by = names(data)][, .N]
cat("   Duplicate rows:", format(duplicate_count, big.mark=","), "\\n")

# Summary table
cat("\\n📋 SUMMARY TABLE:\\n")
summary_dt <- data.table(
    Column = names(data),
    Type = sapply(data, function(x) class(x)[1]),
    Missing = sapply(data, function(x) sum(is.na(x))),
    Unique = sapply(names(data), function(col) data[, uniqueN(get(col), na.rm = TRUE)])
)
print(summary_dt)

cat("\\n")
cat(paste(rep("=", 70), collapse = ""), "\\n")
cat("✅ ANALYSIS COMPLETE\\n")
cat("Report generated:", Sys.time(), "\\n")
cat(paste(rep("=", 70), collapse = ""), "\\n")
'''
        
        with open(script_name, "w") as f:
            f.write(r_content)
        
        return f"""✅ COMPREHENSIVE R ANALYSIS SCRIPT CREATED

📄 Script: {script_name}
📁 Location: {os.getcwd()}
📊 Target: {file_name}

🚀 TO RUN:
"C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe" --vanilla {script_name}

📋 FEATURES:
✅ Automatic package installation
✅ data.table for optimal performance
✅ Automatic separator detection
✅ Comprehensive column analysis
✅ Data quality assessment
✅ Complete dataset display (if small)
✅ Professional formatted output

This script provides R-level analysis equivalent to professional data tools!"""
        
    except Exception as e:
        return f"❌ Error creating R script: {str(e)}"


@mcp.tool()
def create_r_analysis_suite(analysis_type: str, data_description: str) -> str:
    """Create specialized R analysis scripts (exploratory, statistical, visualization)"""
    
    templates = {
        "exploratory": """
# Exploratory Data Analysis
library(data.table)
library(ggplot2)

# Load data (adjust path as needed)
data <- fread("your_data.csv")

cat("=== EXPLORATORY DATA ANALYSIS ===\\n")
cat("Data loaded:", nrow(data), "rows x", ncol(data), "columns\\n\\n")

# Basic structure
cat("=== DATA STRUCTURE ===\\n")
str(data)

cat("\\n=== SUMMARY STATISTICS ===\\n")
summary(data)

cat("\\n=== MISSING VALUES ===\\n")
missing_summary <- data[, lapply(.SD, function(x) sum(is.na(x)))]
print(missing_summary)

cat("\\n=== FIRST FEW ROWS ===\\n")
print(head(data))

cat("\\n=== ANALYSIS COMPLETE ===\\n")
""",
        
        "statistical": """
# Statistical Analysis
library(data.table)
library(stats)

# Load data
data <- fread("your_data.csv")

cat("=== STATISTICAL ANALYSIS ===\\n")

# Descriptive statistics
cat("\\n=== DESCRIPTIVE STATISTICS ===\\n")
numeric_cols <- names(data)[sapply(data, is.numeric)]
if(length(numeric_cols) > 0) {
    for(col in numeric_cols) {
        cat("\\nColumn:", col, "\\n")
        col_data <- data[[col]][!is.na(data[[col]])]
        if(length(col_data) > 0) {
            cat("  Mean:", round(mean(col_data), 3), "\\n")
            cat("  Median:", round(median(col_data), 3), "\\n")
            cat("  SD:", round(sd(col_data), 3), "\\n")
            cat("  Min:", min(col_data), "\\n")
            cat("  Max:", max(col_data), "\\n")
        }
    }
}

# Correlation analysis
if(length(numeric_cols) > 1) {
    cat("\\n=== CORRELATION MATRIX ===\\n")
    cor_matrix <- cor(data[, ..numeric_cols], use="complete.obs")
    print(round(cor_matrix, 3))
}

cat("\\n=== STATISTICAL ANALYSIS COMPLETE ===\\n")
""",
        
        "visualization": """
# Data Visualization
library(data.table)
library(ggplot2)

# Load data
data <- fread("your_data.csv")

cat("=== DATA VISUALIZATION ===\\n")
cat("Creating plots...\\n")

# Basic plots for numeric variables
numeric_cols <- names(data)[sapply(data, is.numeric)]
if(length(numeric_cols) > 0) {
    for(col in numeric_cols[1:min(3, length(numeric_cols))]) {
        cat("Creating histogram for", col, "\\n")
        
        p <- ggplot(data, aes_string(x = col)) +
            geom_histogram(bins = 20, fill = "steelblue", alpha = 0.7) +
            theme_minimal() +
            labs(title = paste("Distribution of", col),
                 x = col, y = "Frequency")
        
        ggsave(paste0("histogram_", col, ".png"), p, width = 8, height = 6)
    }
}

# Categorical plots
char_cols <- names(data)[sapply(data, is.character)]
if(length(char_cols) > 0) {
    for(col in char_cols[1:min(2, length(char_cols))]) {
        if(data[, uniqueN(get(col))] <= 10) {  # Only if reasonable number of categories
            cat("Creating bar plot for", col, "\\n")
            
            p <- ggplot(data, aes_string(x = col)) +
                geom_bar(fill = "coral", alpha = 0.7) +
                theme_minimal() +
                labs(title = paste("Count of", col),
                     x = col, y = "Count") +
                theme(axis.text.x = element_text(angle = 45, hjust = 1))
            
            ggsave(paste0("barplot_", col, ".png"), p, width = 8, height = 6)
        }
    }
}

cat("\\n=== VISUALIZATION COMPLETE ===\\n")
cat("Plot files saved in current directory\\n")
"""
    }
    
    try:
        base_template = templates.get(analysis_type.lower(), templates["exploratory"])
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{analysis_type}_{timestamp}.R"
        
        custom_code = f"""# {analysis_type.title()} Analysis
# Data: {data_description}
# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

{base_template}

# Additional notes: {data_description}
cat("Analysis type:", "{analysis_type}\\n")
cat("Data description:", "{data_description}\\n")
"""
        
        with open(filename, "w") as f:
            f.write(custom_code)
        
        return f"""✅ {analysis_type.title()} Analysis Script Created

📄 Script: {filename}
📊 Type: {analysis_type}
📝 Data: {data_description}

🚀 TO EXECUTE:
"C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe" --vanilla {filename}

Available types: exploratory, statistical, visualization
"""
        
    except Exception as e:
        return f"❌ Error creating analysis suite: {str(e)}"

# =============================================================================
# PROJECT MANAGEMENT TOOLS
# =============================================================================

@mcp.tool()
def list_project_files(path: str = ".") -> str:
    """List files in project directory with smart categorization"""
    try:
        files = []
        for root, dirs, filenames in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]
            
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), path)
                if filename.endswith(('.R', '.py', '.qmd', '.Rmd', '.ipynb')):
                    files.append(f"📄 {rel_path}")
                elif filename.endswith(('.csv', '.json', '.xlsx', '.txt')):
                    files.append(f"📊 {rel_path}")
                else:
                    files.append(f"   {rel_path}")
        
        return f"📁 Project files in {path}:\n" + "\n".join(files[:50])
        
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"


@mcp.tool()
def list_r_scripts() -> str:
    """List all R scripts with metadata"""
    try:
        r_files = [f for f in os.listdir(".") if f.endswith('.R')]
        
        if not r_files:
            return "📄 No R scripts found in current directory."
        
        file_info = []
        for file in sorted(r_files):
            try:
                mod_time = os.path.getmtime(file)
                mod_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mod_time))
                size = os.path.getsize(file)
                
                file_info.append(f"  📄 {file}")
                file_info.append(f"      Size: {size:,} bytes")
                file_info.append(f"      Modified: {mod_time_str}")
                file_info.append("")
            except:
                file_info.append(f"  📄 {file} (metadata unavailable)")
        
        return f"📄 R scripts in {os.getcwd()}:\n\n" + "\n".join(file_info)
        
    except Exception as e:
        return f"❌ Error listing R scripts: {str(e)}"


@mcp.tool()
def create_r_batch_runner(script_names: list[str]) -> str:
    """Create batch file to run multiple R scripts sequentially"""
    try:
        batch_content = """@echo off
echo ===============================================
echo R Script Batch Runner
echo Generated: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """
echo ===============================================
echo.

"""
        
        for script in script_names:
            if script.endswith('.R'):
                batch_content += f'''echo [%TIME%] Running {script}...
"C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe" --vanilla {script}
if errorlevel 1 (
    echo ERROR: {script} failed!
    pause
    exit /b 1
)
echo [%TIME%] Completed {script}
echo -----------------------------------------------
echo.

'''
        
        batch_content += """echo ===============================================
echo All R scripts completed successfully!
echo ===============================================
pause
"""
        
        batch_filename = f"run_r_scripts_{time.strftime('%Y%m%d_%H%M%S')}.bat"
        with open(batch_filename, "w") as f:
            f.write(batch_content)
        
        return f"""✅ Batch runner created: {batch_filename}

🚀 TO EXECUTE:
1. Double-click {batch_filename}
2. Or run in Command Prompt: {batch_filename}

📋 WILL RUN IN ORDER:
{chr(10).join(f"  ✓ {script}" for script in script_names)}

⚙️  Features:
- Error checking and reporting
- Timestamps for each script
- Automatic pause on completion
"""
        
    except Exception as e:
        return f"❌ Error creating batch runner: {str(e)}"

# =============================================================================
# DIAGNOSTIC TOOLS
# =============================================================================

@mcp.tool()
def check_environment() -> str:
    """Check Python libraries and R availability"""
    result = []
    result.append("🔍 ENVIRONMENT CHECK")
    result.append("=" * 30)
    
    # Python libraries
    libraries = ['pandas', 'polars', 'numpy']
    for lib in libraries:
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'unknown')
            result.append(f"✅ {lib}: {version}")
        except ImportError:
            result.append(f"❌ {lib}: Not installed")
    
    # R availability
    r_path = r"C:\Program Files\R\R-4.5.0\bin\Rscript.exe"
    if os.path.exists(r_path):
        result.append(f"✅ R: Available at {r_path}")
    else:
        result.append(f"❌ R: Not found at {r_path}")
    
    # Python version
    import sys
    result.append(f"🐍 Python: {sys.version.split()[0]}")
    
    return "\n".join(result)


@mcp.resource("project://current")
def get_project_overview() -> str:
    """Overview of current project structure"""
    cwd = os.getcwd()
    
    # Count file types
    file_counts = {"R": [], "Python": [], "Data": [], "Other": []}
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.R'):
                file_counts["R"].append(file)
            elif file.endswith('.py'):
                file_counts["Python"].append(file)
            elif file.endswith(('.csv', '.xlsx', '.json')):
                file_counts["Data"].append(file)
            else:
                file_counts["Other"].append(file)
    
    overview = f"""
📁 PROJECT OVERVIEW
Location: {cwd}
Name: {os.path.basename(cwd)}

📊 FILE SUMMARY:
- R files: {len(file_counts["R"])} {f"({', '.join(file_counts['R'][:3])}{'...' if len(file_counts['R']) > 3 else ''})" if file_counts["R"] else ""}
- Python files: {len(file_counts["Python"])} {f"({', '.join(file_counts['Python'][:3])}{'...' if len(file_counts['Python']) > 3 else ''})" if file_counts["Python"] else ""}
- Data files: {len(file_counts["Data"])} {f"({', '.join(file_counts['Data'][:3])}{'...' if len(file_counts['Data']) > 3 else ''})" if file_counts["Data"] else ""}
- Other files: {len(file_counts["Other"])}

🎯 PROJECT TYPE: {
    'Mixed R/Python Analytics' if file_counts["R"] and file_counts["Python"] else
    'R Analytics' if file_counts["R"] else
    'Python Development' if file_counts["Python"] else
    'Data Analysis' if file_counts["Data"] else
    'General'
}
"""
    return overview


if __name__ == "__main__":
    mcp.run()
