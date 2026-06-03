# JSON to CSV Converter

## 📌 Overview:
This project automates the conversion of JSON files into a single CSV file.  
It validates multiple JSON formats (standard, JSONL, dict/list), handles null values, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes logging for error tracking and execution flow.

👉 In short: you provide JSON files, it gives you a clean CSV plus reports.

---

## 🚀 Features:
- Read multiple JSON files at once  
- Support for JSON, JSONL, dict/list structures  
- Automatic encoding detection with **chardet**  
- Null value replacement with `"Not Informed"`  
- Concatenation into a single CSV file  
- JSON and TXT report generation  
- Structured logging with rotating log files  
- Organized output in a `result/` folder  
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

## 📂 Project Structure:
```bash
json_to_csv/
├── json_converter.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── data1.json
├── data2.json
├── data3.json
└── result/
    ├── report.json
    ├── report.txt
    ├── Merge.csv
    ├── process_json.log
    └── errors_json.log
```

---

## ⚙️ How to Run:
Single file:
```bash
python json_converter.py --json_files data1 --output_csv output.csv --json --txt
```
Multiple files:
```bash
python json_converter.py --json_files data1 data2 data3 --output_csv customers.csv --txt
```
Logging options:

- **--log_json** → structured JSON logs

- **--log_txt** → plain text logs (default)

---

## 📊 Example Output
JSON Report:
```json
{
  "report_title": "Report - JSON to CSV Automation",
  "date": "26/05/2026 15:40:00",
  "execution_time_seconds": 0.35,
  "files_success": 3,
  "files_failed": 0,
  "failed_list": [],
  "notes": [
    "JSON files processed and concatenated.",
    "Null values handled.",
    "Final CSV generated successfully."
  ]
}
```

TXT Report

```text
Report - JSON to CSV Automation
Date: 26/05/2026 15:40:00
Execution time: 0.35 seconds

Files processed successfully: 3
Files failed: 0
Failed files: None

Notes:
- JSON files processed and concatenated.
- Null values handled.
- Final CSV generated successfully.
```

---

## 🧠 Internal Functions (for developers)
- open_json() → Opens and validates JSON files with fallback strategies

- handle_null_values() → Replaces nulls with "Not Informed"

- generate_report() → Creates JSON/TXT reports

- save_results() → Moves results and logs to result/ folder

- main() → Controls execution pipeline

---

## 🔒 Error Handling
- Detects encoding errors with chardet

- Handles invalid JSON formats (standard, JSONL, dict/list)

- Tracks failed files with detailed logging

- Structured error logs (errors_json.log or errors_txt.log)

- Critical logging when all files fail

---

## 📌 Technologies Used
- Python 3.12.7

- Pandas

- Chardet

- Argparse

- Logging / RotatingFileHandler

- python-json-logger

---

## ✅ Final Result
- This project is ideal for:

- Data conversion pipelines

- JSON validation

- CSV generation

- Report automation

- Error-tracked batch processing

---

## 🔎 Observations & Recommendations
- Encoding detection: chardet may be imprecise for very small files.

- Concatenation: JSONs with different structures will generate many columns with nulls.

- save_results: overwrites files if they already exist in result/. Add timestamps if versioning is needed.

- Schema validation: not enforced. Add checks if consistency across JSONs is required.

- Duplicates: not removed. Use drop_duplicates() if necessary.

- Exit codes: currently not differentiated. Adding sys.exit(0/1) can improve CI/CD integration.

- Performance: for large volumes of JSONs, consider using Pandas chunks to optimize memory.

---
