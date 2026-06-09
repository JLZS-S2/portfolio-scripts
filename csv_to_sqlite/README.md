# CSV to SQLite Pipeline

## 📌 Overview  
This project automates the validation, cleaning, and import of CSV files into SQLite databases.  
It detects encoding, removes duplicates, handles missing values, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide CSV files, it gives you SQLite databases plus reports.

---

## 🚀 Features
- Validate and open CSV files with encoding detection (chardet)  
- Import cleaned data into SQLite databases  
- Remove duplicates and replace null values with `"Not Informed"` (default)  
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
csv_to_sqlite/
├── csv_to_sqlite.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── sample1.csv
├── sample2.csv
└── result/
    ├── report.json
    ├── report.txt
    ├── sample1.db
    ├── sample2.db
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Process CSV files with TXT report (default):
```bash
python csv_to_sqlite.py --input sample1 sample2 --txt
```

Generate JSON report:
```bash
python csv_to_sqlite.py --input sample1 sample2 --json
```

Custom replacement for missing values:
```bash
python csv_to_sqlite.py --input sample1 sample2 --for_NaN "Unknown" --json --txt
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 📊 Example Output

**JSON Report**
```json
{
  "report_title": "Report - CSV to SQLite",
  "date": "06/06/2026 20:40:00",
  "execution_time_seconds": 0.65,
  "summary": {
    "success": 2,
    "failures": 0,
    "failed_list": []
  },
  "file_records": [
    { "name": "sample1.csv", "records_inserted": 120, "duplicates_ignored": 5 },
    { "name": "sample2.csv", "records_inserted": 80, "duplicates_ignored": 2 }
  ],
  "notes": [
    "CSV imported into SQLite.",
    "Duplicates removed.",
    "Null values handled."
  ]
}
```

**TXT Report**
```text
Report - CSV to SQLite
Date: 06/06/2026 20:40:00
Execution time: 0.65 seconds

Execution Summary:
Success: 2
Failures: 0
Failed files: None

File Records:
- sample1.csv: Records inserted: 120 | Duplicates ignored: 5
- sample2.csv: Records inserted: 80 | Duplicates ignored: 2

Notes:
- CSV imported into SQLite.
- Duplicates removed.
- Null values handled.
```

---

## 🧠 Internal Functions (for developers)
- `open_input()` → Validates and opens CSV files with encoding detection  
- `duplicates_and_nulls()` → Removes duplicates and fills missing values  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves DBs, reports, and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing or invalid CSV files  
- Handles encoding errors gracefully  
- Tracks failed files with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Critical logging when all files fail  

---

## 📌 Technologies Used
- Python 3.12.7  
- Pandas  
- SQLite3  
- Argparse  
- Chardet for encoding detection  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Final Result  
This project is ideal for:
- CSV validation and cleaning  
- Automated database creation  
- Data preprocessing pipelines  
- Report automation  
- Error-tracked batch processing  

---

## 🔎 Observations & Recommendations
- **save_results**: overwrites files if they already exist in `result/`. Add timestamps if versioning is needed.  
- **Encoding detection**: may be imprecise for very small files.  
- **Duplicates**: removed automatically; adjust if you want to keep them.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  

---