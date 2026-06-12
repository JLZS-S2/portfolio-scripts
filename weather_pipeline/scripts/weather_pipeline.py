import requests
from dotenv import load_dotenv
import argparse
import sys
import os
import pandas as pd
import json
import time
from typing import Dict, Any, List
from logging import Logger, Handler
from logging_config import setup_logging
from logging_txt import logging_txt
from datetime import datetime
import shutil
import logging

logger: Logger | None = None


def request_api(city_name: str) -> Dict[str, Any]:
    """Request data from the WEATHER API."""
    logger.info("Starting request_api for city: %s", city_name)
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    if not API_KEY:
        logger.error("API_KEY not found in .env file")
        return {"status": "ERROR", "message": "API_KEY not configured"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    for attempt in range(3):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            logger.info("Request successfully completed for: %s", city_name)
            return {"status": "OK", "data": data}
        except requests.exceptions.Timeout:
            logger.warning("Timeout on attempt %d for city %s", attempt + 1, city_name)
        except requests.exceptions.ConnectionError:
            logger.error("No internet connection on attempt %d", attempt + 1)
        except requests.exceptions.HTTPError:
            status_code = getattr(r, "status_code", None)
            logger.error("HTTP error on attempt %d: %s", attempt + 1, status_code)
            return {"status": "ERROR", "message": f"HTTP error: {status_code}"}
        except requests.exceptions.RequestException as e:
            logger.error("Unexpected error on attempt %d: %s", attempt + 1, e)

    return {"status": "ERROR", "message": f"Failed after 3 attempts for {city_name}"}


def extract_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from API response."""
    information = {
        "name": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "description": data.get("weather", [{}])[0].get("description"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "pressure": data.get("main", {}).get("pressure")
    }
    logger.info("Information extracted: %s", information)
    return information


def generate_report(summary: Dict[str, Any], execution_time: float,
                    json_file: bool = False, txt_file: bool = False) -> None:
    """Generate report in JSON and/or TXT."""
    logger.info("Generating report...")
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - Weather Data Pipeline",
        "date": current_date,
        "execution_time_seconds": round(float(execution_time), 2),
        "summary": summary,
        "notes": [
            "Weather data successfully retrieved from API.",
            "Data exported to CSV and JSON.",
            "Fallback applied for failed cities."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False, default=str)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - Weather Data Pipeline\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Success: {summary.get('success', 0)}\n")
            tf.write(f"Failures: {summary.get('failures', 0)}\n")
            tf.write(f"Failed cities: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n\n")
            tf.write("Notes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(output_files: List[str], reports: List[str]) -> None:
    """Move results and logs to result folder."""
    logger.info("Moving results to 'result' folder...")
    log_type = os.path.exists("process_txt.log")
    log: List[str] = ["process_txt.log", "errors_txt.log"] if log_type else ["process_json.log", "errors_json.log"]

    destination = os.path.join("result")
    os.makedirs(destination, exist_ok=True)

    files: List[str] = output_files + reports + log

    for file in files:
        if file and os.path.exists(file):
            shutil.move(file, os.path.join(destination, os.path.basename(file)))
            logger.info("File moved: %s", file)

    print("- All results have been moved.")


def main() -> None:
    global logger

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_content", required=True, help="Text file containing city names")
    parser.add_argument("--file_csv", default="Data.csv", help="Output CSV file name")
    parser.add_argument("--file_json", default="Data.json", help="Output JSON file name")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    handlers: List[Handler] = []
    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="Weather Data Pipeline")
        logger.info("Logger initialized in JSON mode.")
    else:
        logger, handlers = logging_txt()
        logger.info("Logger initialized in TXT mode.")

    start_time = time.time()
    logger.info("Starting Weather Data Pipeline...")

    file_name = args.file_content if args.file_content.endswith(".txt") else args.file_content + ".txt"
    logger.debug("Input file: %s", file_name)

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            cities = [line.strip() for line in f if line.strip()]
        logger.info("File %s loaded successfully. %d city(ies) found.", file_name, len(cities))
    except FileNotFoundError:
        logger.error("File not found: %s", file_name)
        summary = {"success": 0, "failures": 1, "failed_list": [file_name]}
        execution_time = time.time() - start_time
        generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)
        save_results([], ["report.json" if args.json else "report.txt"])
        sys.exit(1)

    all_data: List[Dict[str, Any]] = []
    errors: List[str] = []

    for city in cities:
        logger.debug("Requesting weather data for city: %s", city)
        info = request_api(city)
        if info["status"] != "OK":
            logger.warning("Failed to retrieve data for city: %s", city)
            errors.append(city)
            continue
        city_data = extract_data(info["data"])
        all_data.append(city_data)
        logger.info("City %s processed successfully.", city)

    if not all_data:
        logger.critical("No city data retrieved. All requests failed.")
        summary = {"success": 0, "failures": len(errors), "failed_list": errors}
        execution_time = time.time() - start_time
        generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)
        pd.DataFrame().to_csv(args.file_csv, index=False)
        pd.DataFrame().to_json(args.file_json, orient="records", indent=4)
        save_results([args.file_csv, args.file_json], ["report.json" if args.json else "report.txt"])
        sys.exit(1)

    df = pd.DataFrame(all_data)
    csv_file = args.file_csv if args.file_csv.endswith(".csv") else args.file_csv + ".csv"
    df.to_csv(csv_file, index=False)
    logger.info("CSV file generated: %s", csv_file)

    json_file = args.file_json if args.file_json.endswith(".json") else args.file_json + ".json"
    df.to_json(json_file, orient="records", indent=4)
    logger.info("JSON file generated: %s", json_file)

    summary = {"success": len(all_data), "failures": len(errors), "failed_list": errors}
    execution_time = time.time() - start_time
    logger.info("Pipeline execution finished in %.2f seconds.", execution_time)
    generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)

    reports: List[str] = []
    if args.json:
        reports.append("report.json")
    if args.txt or (not args.json and not args.txt):
        reports.append("report.txt")

    logging.shutdown()
    for h in logger.handlers[:]:
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass
    for handler in handlers[:]:
        try:
            handler.flush()
            handler.close()
        except Exception:
            pass
        logger.removeHandler(handler)

    output_files = [csv_file, json_file]
    save_results(output_files, reports)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
