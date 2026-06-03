# Merge & Filter CSV Pipeline

## 📌 Overview  
This project automates the merging of multiple CSV files into a single dataset.  
It removes duplicates, handles missing values, applies dynamic filters defined in a JSON file, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide CSV files, it gives you a clean merged/filtered CSV plus reports.

---

## 🚀 Features
- Read multiple CSV files at once  
- Merge into a single dataset  
- Remove duplicates and handle missing values with `"Not Informed"`  
- Apply dynamic filters defined in `filter.json`  
- Export final CSV file  
- JSON and TXT report generation  
- Structured logging with rotating log files (JSON or TXT)  
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

## 📂 Project Structure
```
merge_filter_csv/
├── merge_filter_csv.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── filter.json
├── data1.csv
├── data2.csv
├── data3.csv
└── result/
    ├── report.json
    ├── report.txt
    ├── output.csv
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Merge without filters:
```bash
python merge_filter_csv.py --files_csv data1 data2 data3 --output_csv merged.csv --txt
```

Merge with filters:
```bash
python merge_filter_csv.py --files_csv data1 data2 data3 --output_csv filtered.csv --filter --json
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 🔎 Filter Configuration
Filters are defined by the user in a JSON file (`filter.json`).  
The script reads this file and applies the rules to the merged DataFrame.

⚠️ Important: Column names in the JSON must match the CSV column names exactly — including capitalization and spelling.  
For example, if the CSV column is `Country`, the JSON must also use `"column": "Country"`.  
Using `"country"` or `"COUNTRY"` will not work.

**Example filter.json**
```json
{
  "filters": [
    { "column": "Country", "operator": "==", "value": "Brazil" },
    { "column": "Age", "operator": ">", "value": 25 }
  ]
}
```

**Supported Operators**
- `==` → equality  
- `> < >= <=` → numeric comparisons  
- `contains` → partial string match  

---

## 📊 Example Output

**TXT Report**
```text
Report - Merge & Filter Pipeline
Date: 01/06/2026 20:10:00
Execution time: 0.45 seconds

Execution Summary:
Files processed successfully: 3
Files failed: 0
Failed files: None

Notes:
- CSV files merged.
- Filters applied if provided.
- Fallback applied for errors.
```

**JSON Report**
```json
{
  "report_title": "Report - Merge & Filter Pipeline",
  "date": "01/06/2026 20:10:00",
  "execution_time_seconds": 0.45,
  "summary": {
    "success": 3,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "CSV files merged.",
    "Filters applied if provided.",
    "Fallback applied for errors."
  ]
}
```

---

## 🧠 Internal Functions (for developers)
- `reader_files()` → Opens and validates CSV files  
- `formating_dataframe()` → Removes duplicates and fills missing values  
- `apply_filter()` → Applies filters from `filter.json`  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves results and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing or invalid CSV files  
- Handles invalid filters gracefully  
- Tracks failed files with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Critical logging when all files fail  

---

## 📌 Technologies Used
- Python 3.12.7  
- Pandas  
- Argparse  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Final Result  
This project is ideal for:
- Data cleaning and preprocessing  
- Batch CSV merging  
- Automated filtering pipelines  
- Report automation  
- Error-tracked batch processing  

---

## 🔎 Observations & Recommendations
- **save_results**: overwrites files if they already exist in `result/`. Add timestamps if versioning is needed.  
- **Filters**: ensure column names match exactly to avoid ignored filters.  
- **Duplicates**: removed automatically; adjust if you want to keep them.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  

---