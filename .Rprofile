# Enhanced .Rprofile with error handling (FIXED)
cat("🚀 Initializing project environment...\n")

# Activate renv
tryCatch({
  if (file.exists("renv/activate.R")) {
    source("renv/activate.R")
    cat("✅ renv activated\n")
  }
}, error = function(e) {
  cat("⚠️  renv activation failed:", e$message, "\n")
})

# Python environment setup
setup_python <- function() {
  python_path <- ".venv/Scripts/python.exe"

  if (!file.exists(python_path)) {
    cat("❌ Python virtual environment not found\n")
    cat("   Expected:", python_path, "\n")
    cat("   Setup instructions:\n")
    cat("   1. Open terminal in project directory\n")
    cat("   2. Run: uv venv --python 3.12\n")
    cat("   3. Run: uv add pandas numpy matplotlib jupyter\n")
    return(FALSE)
  }

  tryCatch({
    # Load reticulate
    if (!require(reticulate, quietly = TRUE)) {
      install.packages("reticulate")
      library(reticulate)
    }

    # Configure Python
    use_python(python_path, required = TRUE)

    # Test Python
    py_run_string("import sys")

    cat("✅ Python environment ready\n")

    # Fixed: Safely get Python version
    python_version <- tryCatch({
      as.character(py_version())
    }, error = function(e) {
      "Unknown"
    })

    cat("🐍 Version:", python_version, "\n")

    # Fixed: Safely get Python path
    python_exe <- tryCatch({
      py_config()$python
    }, error = function(e) {
      python_path
    })

    cat("📍 Path:", dirname(python_exe), "\n")

    return(TRUE)

  }, error = function(e) {
    cat("❌ Python setup failed:", e$message, "\n")
    return(FALSE)
  })
}

# Setup Python automatically
python_ready <- setup_python()

# Startup completion message
cat("════════════════════════════════════\n")
cat("📂 Project:", basename(getwd()), "\n")
cat("🔧 renv:", ifelse(file.exists("renv"), "✅", "❌"), "\n")
cat("🐍 Python:", ifelse(python_ready, "✅", "❌"), "\n")

if (python_ready) {
  cat("🎉 Environment ready! Start coding.\n")
} else {
  cat("⚠️  Run check_env() for troubleshooting\n")
}
cat("════════════════════════════════════\n")

# Helper functions
check_env <- function() {
  cat("=== ENVIRONMENT DIAGNOSTICS ===\n")

  # File checks
  cat("Files:\n")
  cat("  .venv/Scripts/python.exe:", file.exists(".venv/Scripts/python.exe"), "\n")
  cat("  pyproject.toml:", file.exists("pyproject.toml"), "\n")
  cat("  uv.lock:", file.exists("uv.lock"), "\n")
  cat("  renv.lock:", file.exists("renv.lock"), "\n")

  # R environment
  cat("\nR Environment:\n")
  cat("  Version:", R.version.string, "\n")
  cat("  Working dir:", getwd(), "\n")

  # Python environment
  if (require(reticulate, quietly = TRUE)) {
    tryCatch({
      cat("\nPython Environment:\n")

      # Safe version check
      version_info <- tryCatch({
        as.character(py_version())
      }, error = function(e) {
        "Unable to determine"
      })
      cat("  Version:", version_info, "\n")

      # Safe executable check
      exe_info <- tryCatch({
        py_config()$python
      }, error = function(e) {
        "Unable to determine"
      })
      cat("  Executable:", exe_info, "\n")

      # Safe virtual env check
      venv_info <- tryCatch({
        py_config()$virtualenv
      }, error = function(e) {
        "Unable to determine"
      })
      cat("  Virtual env:", venv_info, "\n")

      # Test imports
      py_run_string("
import sys
try:
    import pandas, numpy, matplotlib
    print('  Packages: ✅ pandas, numpy, matplotlib')
except ImportError as e:
    print(f'  Packages: ❌ {e}')
")
    }, error = function(e) {
      cat("  Status: ❌", e$message, "\n")
    })
  } else {
    cat("\nPython: ❌ reticulate not available\n")
  }
}

fix_python <- function() {
  cat("🔧 Python Environment Setup Instructions:\n")
  cat("1. Open terminal in project directory\n")
  cat("2. Run: uv venv --python 3.12\n")
  cat("3. Run: uv add pandas numpy matplotlib jupyter\n")
  cat("4. Restart RStudio\n")
  cat("5. Run: check_env()\n")
}
