import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Union

import pandas as pd
from logging import Logger, Handler

from logging_config import setup_logging
from logging_txt import logging_txt


logger: Logger | None = None


def reader_files(files: List[str]) -> Dict[str, Union[str, Any]]:
    """Open CSV files and validate formats. Returns DataFrames for further operations."""
    result = []
    failures = 0
    failed_list = []
    failure_limit = 2

    for file in files:
        try:
            df = pd.read_csv(file)
            result.append(df)
            logger.info("File %s successfully read.", file)
        except Exception as e:
            failures += 1
            failed_list.append(file)
            logger.error("Error reading %s: %s", file, e)

            if failures >= failure_limit:
                return {
                    "status": "ERROR",
                    "message": "Files not found or invalid.",
                    "failed_list": failed_list
                }
            else:
                logger.warning("Continuing with next file after failure.")
                continue

    logger.info("Finished. Files processed: %s", len(result))
    return {
        "status": "OK",
        "data": result,
        "failures": failures,
        "failed_list": failed_list
    }


def formating_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format and prepare the final CSV: remove duplicates and handle missing values."""
    df = dataframe.drop_duplicates()
    if df.isna().any().any():
        logger.info("Empty fields identified. Filling with 'Not Informed'.")
        df = df.fillna("Not Informed")
    return df


def apply_filter(df: pd.DataFrame, filters: List[Dict[str, Any]]) -> pd.DataFrame:
    """Apply filters defined in filter.json"""
    for f in filters:
        col, op, val = f["column"], f["operator"], f["value"]
        if col not in df.columns:
            logger.warning("Column %s not found, filter ignored.", col)
            continue
        try:
            if op == "contains":
                df = df[df[col].astype(str).str.contains(str(val), case=False)]
            else:
                expr = f"{col} {op} @val"
                df = df.query(expr)
        except Exception as e:
            logger.error("Error applying filter %s %s %s: %s", col, op, val, e)
    return df


def generate_report(summary: Dict[str, Any], execution_time: float,
                    json_file: bool = False, txt_file: bool = False) -> None:
    """Generate report in JSON and/or TXT"""
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report = {
        "report_title": "Report - Merge & Filter Pipeline",
        "date": current_date,
        "execution_time_seconds": round(execution_time, 2),
        "summary": summary,
        "notes": [
            "CSV files merged.",
            "Filters applied if provided.",
            "Fallback applied for errors."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - Merge & Filter Pipeline\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Files processed successfully: {summary.get('success', 0)}\n")
            tf.write(f"Files failed: {summary.get('failures', 0)}\n")
            tf.write(f"Failed files: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(output_file: str, reports: List[str]) -> None:
    """Move results and logs to result folder"""
    log_type = os.path.exists("process_json.log")
    log: List[str] = ["process_json.log", "errors_json.log"] if log_type else ["process_txt.log", "errors_txt.log"]

    destination = Path("result")
    destination.mkdir(exist_ok=True)

    files: List[str] = [output_file] + reports + log

    for file in files:
        if file and os.path.exists(file):
            target = destination / file
            if target.exists():
                if target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
            shutil.move(file, target)


def main() -> None:
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--files_csv", nargs="+", required=True, help="CSV files to process")
    parser.add_argument("--output_csv", default="output.csv", help="Final CSV file name")
    parser.add_argument("--filter", action="store_true", help="Apply filter if filter.json exists")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    global logger
    handlers: List[Handler] = []

    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="Merge & Filter Pipeline")
    else:
        logger, handlers = logging_txt()

    args.files_csv = [f if f.endswith(".csv") else f + ".csv" for f in args.files_csv]
    args.output_csv = args.output_csv if args.output_csv.endswith(".csv") else args.output_csv + ".csv"

    if len(args.files_csv) <= 1:
        logger.error("Impossible to proceed with less than two files.")
        summary = {"success": 0, "failures": len(args.files_csv), "failed_list": args.files_csv}
        execution_time = time.time() - start_time
        generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)
        save_results(args.output_csv, ["report.json" if args.json else "report.txt"])
        sys.exit(1)

    reader_info = reader_files(args.files_csv)
    if reader_info["status"] == "OK":
        all_files = pd.concat(reader_info["data"])
        df = formating_dataframe(all_files)

        if args.filter:
            try:
                with open("filter.json", "r", encoding="utf-8") as f:
                    filters = json.load(f)["filters"]
                df = apply_filter(df, filters)
                logger.info("Filters applied successfully.")
            except Exception as e:
                logger.warning("Could not apply filter: %s", e)

        df.to_csv(args.output_csv, index=False)
        logger.info("Final CSV generated: %s", args.output_csv)

        summary = {
            "success": len(reader_info["data"]),
            "failures": reader_info["failures"],
            "failed_list": reader_info["failed_list"]
        }
    else:
        logger.error("Error processing files: %s", reader_info.get("message", ""))
        summary = {
            "success": 0,
            "failures": len(reader_info.get("failed_list", [])),
            "failed_list": reader_info.get("failed_list", [])
        }

    execution_time = time.time() - start_time
    generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)

    # Close handlers to release log files
    for handler in handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
    for h in logger.handlers[:]:
        h.flush()
        h.close()
        logger.removeHandler(h)

    if args.json and args.txt:
        reports = ["report.json", "report.txt"]
    elif args.json:
        reports = ["report.json"]
    else:
        reports = ["report.txt"]

    save_results(args.output_csv, reports)
    logger.info("Execution finished")


if __name__ == "__main__":
    main()