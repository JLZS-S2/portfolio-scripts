# File Organizer Pipeline

## 📌 Overview  
This project automates file organization by extension.  
It moves or copies files from an original folder into organized subfolders, counts files by extension, compresses the organized folder into a ZIP, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide a folder with files, it gives you an organized structure plus reports.

---

## 🚀 Features
- Organize files by extension into subfolders  
- Handle unmapped extensions in `OTHERS`  
- Move or copy files (default: copy)  
- Count files by extension with logging  
- Compress organized folder into ZIP  
- JSON and TXT report generation  
- Structured logging with rotating log files  
- Organized output in a `result/` folder  
- Error tracking with detailed failed item list  

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
file_automation/
├── file_automation.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── extension.json
├── sample_files/
│   ├── file1.csv
│   ├── file2.txt
│   ├── image.png
│   └── doc.pdf
└── result/
    ├── report.json
    ├── report.txt
    ├── Organized files
    ├── Organized files.zip
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Organize with copy (default):
```bash
python file_automation.py --folder_original sample_files --folder_organized "Organized files" --extensions csv:csv txt:txt png:images pdf:docs --txt
```

Organize with move:
```bash
python file_automation.py --folder_original sample_files --folder_organized "Organized files" --extensions csv:csv txt:txt png:images pdf:docs --move_files --json
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 📊 Example Output

**TXT Report**
```text
Report - File Organizer Pipeline
Date: 28/05/2026 16:40:00
Execution time: 0.55 seconds

Execution Summary:
Success: 1
Failures: 0
Failed items: None

File Counts:
- csv: 2 files
- txt: 1 files
- png: 1 files
- pdf: 1 files

Notes:
- Files organized by extension.
- Files counted by extension.
- Organized folder compressed into ZIP.
- Fallback applied for errors.
```

---

## 🧠 Internal Functions (for developers)
- `organizer()` → Organizes files by extension  
- `counter()` → Counts files by extension  
- `zip_folder()` → Compresses organized folder  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves results and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing folders  
- Handles unmapped extensions  
- Tracks failed items  
- Structured error logs (`errors.log` or `errors_txt.log`)  
- Critical logging when execution fails  

---

## 📌 Technologies Used
- Python 3.12.7  
- Argparse  
- Logging / RotatingFileHandler  
- Zipfile  
- JSON  

---

## ✅ Final Result  
This project is ideal for:
- File organization  
- Batch processing  
- Automated archiving  
- Report generation  
- Error-tracked pipelines  

---

## 🔎 Observations & Recommendations
- **save_results**: overwrites files if they already exist in `result/`. Add timestamps if versioning is needed.  
- **Large folders**: compression may take longer; consider splitting into chunks.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  
- **Extension mapping**: ensure `extension.json` is consistent to avoid misplacement.  

---