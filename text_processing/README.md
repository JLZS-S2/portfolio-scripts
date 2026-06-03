# Text Processing Automation

## 📌 Overview  
This project automates the cleaning and processing of text files.  
It removes blank lines, splits content by multiple keywords, counts lines and words, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `results/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide TXT files, it gives you cleaned, split files plus reports.

---

## 🚀 Features
- Automatic blank line removal  
- Keyword-based text splitting (supports multiple keywords)  
- Line and word counting per file  
- JSON and TXT report generation  
- Structured logging with rotating log files (JSON or TXT)  
- Organized output in a `results/` folder  
- Encoding detection with **chardet**  
- Error tracking with detailed failed file list  

---

## 📋 Requirements
- Python 3.12+  
- Dependencies listed in `requirements.txt`  

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
text_processing/
├── text_processing.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── sample1.txt
├── sample2.txt
└── result/
    ├── report.json
    ├── report.txt
    ├── cleaned_files/
    │   ├── new_sample1.txt
    │   └── new_sample2.txt
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Single file:
```bash
python text_processing.py --file sample1 --keywords DATA WORD --json --txt
```

Multiple files:
```bash
python text_processing.py --file sample1 sample2 --keywords DATA KEY --txt
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 📊 Example Output

**JSON Report**
```json
{
  "report_title": "Report - Text Processing Automation",
  "date": "01/06/2026 21:30:00",
  "execution_time_seconds": 0.42,
  "files": {
    "new_sample1.txt": { "lines": 12, "words": 95 },
    "new_sample2.txt": { "lines": 8, "words": 60 }
  },
  "summary": {
    "success": 2,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "All files were cleaned and split by keyword.",
    "Reports generated in JSON and TXT formats.",
    "Files moved to organized folders.",
    "Fallback applied for errors."
  ]
}
```

**TXT Report**
```text
Report - Text Processing Automation
Date: 01/06/2026 21:30:00
Execution time: 0.42 seconds

Summary of processed files:
- new_sample1.txt: 12 lines, 95 words
- new_sample2.txt: 8 lines, 60 words

Execution Summary:
Files processed successfully: 2
Files failed: 0
Failed files: None

Notes:
- All files were cleaned and split by keyword.
- Reports generated in JSON and TXT formats.
- Files moved to organized folders.
- Fallback applied for errors.
```

---

## 🧠 Internal Functions (for developers)
- `clean_text()` → Removes blank lines and detects encoding  
- `split_keywords()` → Splits text using multiple keywords  
- `count_lines_words()` → Counts lines and words per file  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves results and logs to `results/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects encoding errors with **chardet**  
- Handles invalid or unreadable TXT files  
- Tracks failed files with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Critical logging when all files fail  

---

## 📌 Technologies Used
- Python 3.12.7  
- Argparse  
- Logging / RotatingFileHandler  
- JSON / Regex  
- Chardet for encoding detection  
- python-json-logger  

---

## ✅ Final Result  
This project is ideal for:
- Text automation  
- Batch TXT processing  
- Data cleaning  
- Report generation  
- Error-tracked pipelines  

---

## 🔎 Observations & Recommendations
- **save_results**: overwrites files if they already exist in `results/`. Add timestamps if versioning is needed.  
- **Keywords**: ensure they are chosen carefully to avoid excessive splitting.  
- **Encoding detection**: may be imprecise for very small files.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  

---