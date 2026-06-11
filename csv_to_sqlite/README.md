# CSV to SQLite Pipeline

## 📌 Overview  
This project automates the validation, cleaning, and import of CSV files into SQLite databases.  
It detects encoding, removes duplicates, handles missing values, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide CSV files in the `ENTRADA/` folder, it gives you SQLite databases plus reports in `result/`.

---

## 🚀 Features
- Validate and open CSV files with encoding detection (chardet)  
- Import cleaned data into SQLite databases  
- Remove duplicates and replace null values with `"Not Informed"` (default)  
- JSON and TXT report generation  
- Structured logging with JSON or TXT format  
- Organized output in a `result/` folder  
- Error tracking with detailed failed file list  
- Interactive launcher (`launcher.py`) and `.bat` script for easy execution  

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
├── scripts/
│   ├── csv_to_sqlite.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   ├── logging_config.json
│   └── __pycache__/
├── ENTRADA/
│   └── data.csv
├── result/
│   ├── report.json
│   ├── report.txt
│   ├── data.db
│   ├── process_txt.log
│   └── errors_txt.log
├── launcher.py
├── run_pipeline.bat
├── requirements.txt
└── LEIAME.txt
```

---

## ⚙️ How to Run
1. Place your CSV files inside the `ENTRADA/` folder.  
2. Double-click `run_pipeline.bat`.  
3. The launcher will ask for optional customization:
   - Replacement for missing values (default: `"Not Informed"`)  
   - Report type (`txt` default, or `json`)  
   - Log type (`txt` default, or `json`)  
   - If you just press **Enter**, defaults are used.  

---

## 📊 Example Output

**JSON Report**
```json
{
  "report_title": "Report - CSV to SQLite",
  "date": "11/06/2026 11:30:00",
  "execution_time_seconds": 1.26,
  "summary": {
    "success": 1,
    "failures": 0,
    "failed_list": []
  },
  "file_records": [
    { "name": "data.csv", "records_inserted": 3, "duplicates_ignored": 1 }
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
Date: 11/06/2026 11:30:00
Execution time: 1.26 seconds

Execution Summary:
Success: 1
Failures: 0
Failed files: None

File Records:
- data.csv: Records inserted: 3 | Duplicates ignored: 1

Notes:
- CSV imported into SQLite.
- Duplicates removed.
- Null values handled.
```

---

## 🧠 Internal Functions (for developers)
- `open_input()` → Validates and opens CSV files with encoding detection  
- `duplicates_and_nulls()` → Removes duplicates and fills missing values  
- `generate_report()` → Creates JSON/TXT reports (now serializes NumPy types safely)  
- `save_results()` → Moves DBs, reports, and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing or invalid CSV files  
- Handles encoding errors gracefully  
- Tracks failed files with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Critical logging when all files fail  
- Safe JSON serialization for Pandas/NumPy types  

---

## 📌 Technologies Used
- Python 3.12.7  
- Pandas  
- SQLite3  
- Argparse  
- Chardet for encoding detection  
- Logging / JSON logger  

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
- **Defaults**: pressing Enter in the launcher uses `"Not Informed"` for nulls, TXT for reports, TXT for logs.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  