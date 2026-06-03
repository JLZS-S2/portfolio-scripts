```markdown
# Weather Data Pipeline (API Integration)

## 📌 Overview  
This project integrates with the OpenWeather API to retrieve weather data for multiple cities.  
It extracts key fields, exports results to CSV and JSON, and generates structured reports in JSON and/or TXT formats.  
The pipeline organizes results into a dedicated `result/` folder and includes structured logging for error tracking and execution flow.

👉 In short: you provide a list of cities, it gives you weather data plus reports.

---

## 🚀 Features
- API integration with OpenWeather  
- Retry mechanism (3 attempts per city)  
- Extraction of temperature, humidity, description, wind speed, feels_like, pressure  
- Export to CSV and JSON  
- JSON and TXT report generation  
- Structured logging with rotating log files (JSON or TXT)  
- Environment variable support via `.env`  
- Organized output in a `result/` folder  
- Error tracking with detailed failed city list  

---

## 📋 Requirements
- Python 3.12+  
- Dependencies listed in `requirements.txt`  
- `.env` file with:  
  ```
  API_KEY=your_openweather_api_key
  ```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
weather_pipeline/
├── weather_pipeline.py
├── logging_config.py
├── logging.txt.py
├── logging_config.json
├── requirements.txt
├── .env
├── cities.txt
└── result/
    ├── report.json
    ├── report.txt
    ├── Data.csv
    ├── Data.json
    ├── process_txt.log
    └── errors_txt.log
```

---

## ⚙️ How to Run
Example with default outputs:
```bash
python weather_pipeline.py --file_content cities.txt --json --txt
```

Custom output names:
```bash
python weather_pipeline.py --file_content cities.txt --file_csv weather.csv --file_json weather.json --txt
```

Logging options:
- `--log_json` → structured JSON logs  
- `--log_txt` → plain text logs (default)  

---

## 📊 Example Output

**JSON Report**
```json
{
  "report_title": "Report - Weather Data Pipeline",
  "date": "02/06/2026 11:20:00",
  "execution_time_seconds": 1.25,
  "summary": {
    "success": 5,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "Weather data successfully retrieved from API.",
    "Data exported to CSV and JSON.",
    "Fallback applied for failed cities."
  ]
}
```

**TXT Report**
```text
Report - Weather Data Pipeline
Date: 02/06/2026 11:20:00
Execution time: 1.25 seconds

Cities processed successfully: 5
Cities failed: 0
Failed cities: None

Notes:
- Weather data successfully retrieved from API.
- Data exported to CSV and JSON.
- Fallback applied for failed cities.
```

---

## 🧠 Internal Functions (for developers)
- `request_api()` → Requests weather data with retries  
- `extract_data()` → Extracts key fields from API response  
- `generate_report()` → Creates JSON/TXT reports  
- `save_results()` → Moves results and logs to `result/` folder  
- `main()` → Controls execution pipeline  

---

## 🔒 Error Handling
- Detects missing `API_KEY`  
- Handles timeouts, connection errors, HTTP errors  
- Tracks failed cities with detailed logging  
- Structured error logs (`errors_json.log` or `errors_txt.log`)  
- Exports empty CSV/JSON if all cities fail  

---

## 📌 Technologies Used
- Python 3.12.7  
- Requests  
- Pandas  
- Dotenv  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Final Result  
This project is ideal for:
- API integration  
- Weather data analysis  
- Data export automation  
- Report generation  
- Error-tracked pipelines  

---

## 🔎 Observations & Recommendations
- **Data overwrite**: CSV and JSON outputs are overwritten each run. If you need versioning, add timestamps to filenames.  
- **API limits**: OpenWeather has rate limits; batch requests may require delays.  
- **Encoding**: UTF-8 is enforced for reports and outputs.  
- **Exit codes**: currently not differentiated. Adding `sys.exit(0/1)` improves CI/CD integration.  
```

---