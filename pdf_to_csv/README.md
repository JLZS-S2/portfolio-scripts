# PDF to CSV Pipeline

## 📌 Overview  
This project automates the extraction of tables and text from PDF files, converting them into structured CSV datasets.  
It validates PDF files, detects separators automatically, handles null values, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide PDF files, it gives you CSV files plus reports.

---

## 🚀 Features
- Validate PDF files (detects missing, protected, or invalid PDFs)  
- Extract tables and text from PDF pages  
- Automatic separator detection for text blocks  
- Convert extracted data into CSV format  
- Replace null values with `"Not Informed"` (default)  
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
pdf_to_csv/
├── pdf_to_csv.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── sample1.pdf
├── sample2.pdf
└── result/
    ├── report.json
    ├── report.txt
    ├── output.csv
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Process PDFs with TXT report (default):
```bash
python pdf_to_csv.py --files sample1 sample2 --txt
```

Generate JSON report:
```bash
python pdf_to_csv.py --files sample1 sample2 --json
```

Custom replacement for missing values:
```bash
python pdf_to_csv.py --files sample1 sample2 --for_NaN "Unknown" --json --txt
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 📊 Example Output

**JSON Report**
```json
{
  "report_title": "Report - PDF to CSV",
  "date": "06/06/2026 21:00:00",
  "execution_time_seconds": 0.75,
  "summary": {
    "success": 2,
    "failures": 0,
    "failed_list": []
  },
  "file_records": [
    { "name": "output.csv", "records_inserted": 250 }
  ],
  "notes": [
    "PDF extracted into CSV.",
    "Tables and text processed.",
    "Null values handled."
  ]
}
```

**TXT Report**
```text
Report - PDF to CSV
Date: 06/06/2026 21:00:00
Execution time: 0.75 seconds

Execution Summary:
Success: 2
Failures: 0
Failed files: None

File Records:
- output.csv: Records inserted: 250

Notes:
- PDF extracted into CSV.
- Tables and text processed.
- Null values handled.
```

---

## 🧠 Internal Functions (for developers)
- `open_pdfs()` → Validates PDF files  
- `parse_text_block()` → Detects separators and parses text into dicts  
- `type_identification()` → Extracts tables or text from PDFs  
- `null_values()` → Replaces null values in DataFrame  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves CSVs, reports, and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing, protected, or invalid PDF files  
- Handles separator detection failures gracefully  
- Tracks failed files with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Critical logging when all files fail  

---

## 📌 Technologies Used
- Python 3.12.7  
- Pandas  
- pdfplumber  
- PyPDF  
- Argparse  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Final Result  
This project is ideal for:
- PDF table/text extraction  
- Automated CSV generation  
- Data cleaning pipelines  
- Report automation  
- Error-tracked batch processing  

---

## 🔎 Observations & Recommendations
- **save_results**: overwrites files if they already exist in `result/`. Add timestamps if versioning is needed.  
- **Separator detection**: may fail for irregular text blocks; defaults to comma.  
- **Null values**: replaced automatically; adjust replacement string if needed.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  

---
