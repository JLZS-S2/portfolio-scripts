import argparse
import chardet
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Union

import pandas as pd
from logging import Logger, Handler

from logging_config import setup_logging
from logging_txt import logging_txt


logger: Logger | None = None


def open_json(files: List[str]) -> Dict[str, Any]:
    """Open JSON files and validate content"""
    all_data: List[pd.DataFrame] = []
    failed_list: List[str] = []
    failures: int = 0

    for file in files:
        with open(file, "rb") as f:
            raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        encoding: str | None = result.get("encoding")

        try:
            df = pd.read_json(file, encoding=encoding)
            all_data.append(df)
            logger.info("File %s successfully read as JSON.", file)
        except ValueError:
            logger.warning("File %s is not valid JSON, attempting raw text.", file)
            try:
                df = pd.read_json(file, encoding=encoding, lines=True)
                all_data.append(df)
                logger.info("File %s successfully read as JSONL", file)
            except ValueError:
                try:
                    with open(file, "r", encoding=encoding) as f:
                        data = json.load(f)
                    df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)
                    all_data.append(df)
                    logger.info("File %s successfully validated", file)
                except Exception as e:
                    failures += 1
                    failed_list.append(file)
                    logger.error("Error reading %s: %s", file, e)
                    continue
        except FileNotFoundError:
            failures += 1
            failed_list.append(file)
            logger.error("File %s not found.", file)
            continue
        except Exception as e:
            failures += 1
            failed_list.append(file)
            logger.error("Unexpected error processing %s: %s", file, e)
            continue

    if failures == len(files):
        logger.critical("All files failed.")
        return {"status": "ERROR", "failures": failures, "failed_list": failed_list}

    return {"status": "OK", "files": all_data, "failures": failures, "failed_list": failed_list}


def handle_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace null values with 'Not Informed'"""
    if df.isna().any().any():
        logger.info("Null values found. Replacing with 'Not Informed'.")
        df = df.fillna("Not Informed")
    return df


def generate_report(summary: Dict[str, Any], execution_time: float,
                    json_file: bool = False, txt_file: bool = False) -> None:
    """Generate report in JSON and/or TXT"""
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - JSON to CSV Automation",
        "date": current_date,
        "execution_time_seconds": round(execution_time, 2),
        "files_success": summary["success"],
        "files_failed": summary["failures"],
        "failed_list": summary["failed_list"],
        "notes": [
            "JSON files processed and concatenated.",
            "Null values handled.",
            "Final CSV generated successfully."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - JSON to CSV Automation\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write(f"Files processed successfully: {summary['success']}\n")
            tf.write(f"Files failed: {summary['failures']}\n")
            tf.write(f"Failed files: {', '.join(summary['failed_list']) if summary['failed_list'] else 'None'}\n")
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
            path_complet = destination / file
            shutil.move(file, path_complet)


def main() -> None:
    start_time: float = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_files", nargs="+", required=True, help="JSON file names")
    parser.add_argument("--output_csv", help="CSV output name", default="Merge.csv")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    global logger
    handlers: List[Handler] = []

    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="JSON to CSV Automation")
    else:
        logger, handlers = logging_txt()

    args.json_files = [f if f.endswith(".json") else f + ".json" for f in args.json_files]
    if not args.output_csv.endswith(".csv"):
        args.output_csv += ".csv"

    open_files = open_json(args.json_files)

    if open_files["status"] == "OK":
        concatenated_df = pd.concat(open_files["files"], ignore_index=True)
        final_df = handle_null_values(concatenated_df)
        final_df.to_csv(args.output_csv, encoding="utf-8", index=False)
        logger.info("CSV %s successfully generated.", args.output_csv)

        summary = {
            "success": len(open_files["files"]),
            "failures": open_files["failures"],
            "failed_list": open_files["failed_list"]
        }
    else:
        summary = {
            "success": 0,
            "failures": open_files["failures"],
            "failed_list": open_files["failed_list"]
        }

    execution_time: float = time.time() - start_time
    generate_report(summary, execution_time, json_file=args.json, txt_file=args.txt)
    
    # principal
    for h in logger.handlers[:]:
        h.flush()
        h.close()
        logger.removeHandler(h)
        
    # second handlers 
    for handler in handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

    
    if args.json and args.txt:
        reports = ["report.json", "report.txt"]
    elif args.json:
        reports = ["report.json"]
    else:  
        reports = ["report.txt"]

    save_results(args.output_csv, reports)


if __name__ == "__main__":
    main()