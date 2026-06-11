import argparse
import pandas as pd
import chardet
import sqlite3
import json
import os
import shutil
import time
from datetime import datetime
from typing import Dict, Any, List, Tuple
from logging import Logger, Handler
from logging_config import setup_logging
from logging_txt import logging_txt
import logging

logger: Logger | None = None


def open_input(files: List[str]) -> Dict[str, Any]:
    logger.info("Starting validation of %d CSV files", len(files))
    success_files: List[Tuple[str, pd.DataFrame]] = []
    failed_files: List[str] = []
    failures = 0

    for file in files:
        try:
            with open(file, "rb") as f:
                raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result['encoding']

            df = pd.read_csv(file, sep=None, engine="python", encoding=encoding)
            success_files.append((file, df))
            logger.info("File successfully validated: %s", file)

        except FileNotFoundError:
            failures += 1
            logger.error("File not found: %s", file)
            failed_files.append(file)
        except PermissionError:
            failures += 1
            logger.error("Permission denied: %s", file)
            failed_files.append(file)
        except Exception as e:
            failures += 1
            logger.error("Unexpected error in %s: %s", file, e)
            failed_files.append(file)

    logger.info("Validation completed: %d success(es), %d failure(s)", len(success_files), failures)

    if failures == len(files):
        logger.critical("All files failed.")
        return {"status": "ERROR", "files": [], "failures": failures, "failed_list": failed_files}

    return {"status": "OK", "files": success_files, "validated": len(success_files),
            "failures": failures, "failed_list": failed_files}


def duplicates_and_nulls(files: List[Tuple[str, pd.DataFrame]], null_replacement: str) -> Dict[str, Any]:
    duplicates: List[Dict[str, Any]] = []
    records: List[Dict[str, Any]] = []
    dfs: List[Tuple[str, pd.DataFrame]] = []

    for file_name, df in files:
        logger.info("Processing file: %s", file_name)
        start_file = time.time()

        mask_duplicates = df.duplicated(keep="first")
        duplicates_count = int(mask_duplicates.sum())

        if df.isna().any().any():
            null_cols = df.columns[df.isna().any()].tolist()
            logger.warning("Null values detected in %s, columns: %s", file_name, null_cols)
            df = df.fillna(null_replacement)
            logger.info("Null values replaced by '%s'", null_replacement)

        df_clean = df.drop_duplicates(keep="first")
        dfs.append((file_name, df_clean))

        info = {
            "name": file_name,
            "records_inserted": int(len(df_clean)),
            "duplicates_ignored": duplicates_count
        }
        records.append(info)

        if duplicates_count > 0:
            duplicates.extend(df[mask_duplicates].to_dict(orient="records"))
            logger.debug("Duplicates ignored in %s: %d", file_name, duplicates_count)

        logger.info("Summary of file %s: Records %d, Duplicates %d. Time: %.2fs",
                    file_name, len(df_clean), duplicates_count, time.time() - start_file)

    logger.info("Cleaning completed. Total records: %d", sum(r["records_inserted"] for r in records))
    return {"dfs": dfs, "duplicates": duplicates, "info": records}


def generate_report(summary: Dict[str, Any], execution_time: float,
                    records: List[Dict[str, Any]],
                    json_file: bool = False, txt_file: bool = False) -> None:
    logger.info("Generating report...")
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - CSV to SQLite",
        "date": current_date,
        "execution_time_seconds": round(float(execution_time), 2),
        "summary": summary,
        "file_records": records,
        "notes": [
            "CSV imported into SQLite.",
            "Duplicates removed.",
            "Null values handled."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False, default=str)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - CSV to SQLite\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Success: {summary.get('success', 0)}\n")
            tf.write(f"Failures: {summary.get('failures', 0)}\n")
            tf.write(f"Failed files: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n\n")
            tf.write("File Records:\n")
            for r in records:
                tf.write(f"- {r['name']}: Records inserted: {r['records_inserted']} | Duplicates ignored: {r['duplicates_ignored']}\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(output_files: List[str], reports: List[str]) -> None:
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
    parser.add_argument("--input", required=True, nargs="+", help="CSV files to process")
    parser.add_argument("--for_NaN", default="Not Informed", help="Replacement for missing values")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    handlers: List[Handler] = []
    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="CSV to SQLite Pipeline")
        logger.info("Logger initialized in JSON mode.")
    else:
        logger, handlers = logging_txt()
        logger.info("Logger initialized in TXT mode.")

    start_time = time.time()
    logger.info("Starting CSV to SQLite conversion pipeline...")

    args.input = [f if f.lower().endswith(".csv") else f + ".csv" for f in args.input]
    logger.debug("Files to process: %s", args.input)

    files_validated = open_input(args.input)
    if files_validated["status"] == "OK":
        logger.info("File validation successful. %d file(s) ready for processing.", len(files_validated["files"]))

        processed = duplicates_and_nulls(files_validated["files"], args.for_NaN)
        final_df = processed["dfs"]

        output_files: List[str] = []
        for file_name, df in final_df:
            db_name = file_name.replace(".csv", ".db")
            conn = sqlite3.connect(db_name)
            df.to_sql("data", conn, if_exists="replace", index=False)
            conn.close()
            logger.info("File %s saved as %s", file_name, db_name)
            output_files.append(db_name)

        summary = {
            "success": int(len(final_df)),
            "failures": int(files_validated["failures"]),
            "failed_list": files_validated["failed_list"]
        }
        records = processed["info"]
    else:
        logger.error("File validation failed. No files processed.")
        summary = {
            "success": 0,
            "failures": int(files_validated["failures"]),
            "failed_list": files_validated["failed_list"]
        }
        records = []
        output_files = []

    execution_time = time.time() - start_time
    logger.info("Pipeline execution finished in %.2f seconds.", execution_time)
    generate_report(summary, execution_time, records=records, json_file=args.json, txt_file=args.txt)

    reports: List[str] = []
    if args.json:
        reports.append("report.json")
    if args.txt or (not args.json and not args.txt):
        reports.append("report.txt")

    # Close handlers
    logging.shutdown()
    for h in logger.handlers[:]:
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

    # Save results
    save_results(output_files, reports)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()