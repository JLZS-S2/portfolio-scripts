import argparse
import pandas as pd
import chardet
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple
from logging import Logger, Handler
from logging_config import setup_logging
from logging_txt import logging_txt
import logging

logger: Logger | None = None


def open_input(files: List[str]) -> Dict[str, Any]:
    """Validate and open multiple CSV files, detecting encoding and returning DataFrames."""
    logger.info("Starting validation of %d CSV files", len(files))
    success_files: List[Tuple[str, pd.DataFrame]] = []
    failed_files: List[str] = []
    failures = 0

    for file in files:
        try:
            with open(file, "rb") as f:
                raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

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


def clean_and_merge(files: List[Tuple[str, pd.DataFrame]], null_replacement: str = "Not Informed") -> Dict[str, Any]:
    dfs: List[pd.DataFrame] = []
    records: List[Dict[str, Any]] = []
    duplicates_total = 0

    for file_name, df in files:
        logger.info("Processing file: %s", file_name)
        start_file = time.time()

        # Detect duplicates
        mask_duplicates = df.duplicated(keep="first")
        duplicates_count = int(mask_duplicates.sum())
        duplicates_total += duplicates_count

        # Handle nulls
        if df.isna().any().any():
            null_cols = df.columns[df.isna().any()].tolist()
            logger.warning("Null values detected in %s, columns: %s", file_name, null_cols)
            df = df.fillna(null_replacement)

        # Keep cleaned dataframe
        dfs.append(df)

        info = {
            "name": file_name,
            "records": int(len(df)),
            "duplicates_ignored": duplicates_count
        }
        records.append(info)

        logger.info("Summary %s: Records %d, Duplicates %d. Time: %.2fs",
                    file_name, len(df), duplicates_count, time.time() - start_file)

    # Merge all DataFrames
    merged_df = pd.concat(dfs, ignore_index=True)

    # Apply global cleaning
    merged_df = merged_df.drop_duplicates(keep="first")
    merged_df = merged_df.fillna(null_replacement)

    logger.info("Merge completed. Total records: %d | Duplicates ignored: %d",
                len(merged_df), duplicates_total)

    return {"df": merged_df, "info": records}



def apply_filter(df: pd.DataFrame, filters: List[Dict[str, Any]]) -> pd.DataFrame:
    """Apply filters defined in filter.json."""
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
            logger.info("Filter applied: %s %s %s", col, op, val)
        except Exception as e:
            logger.error("Error applying filter %s %s %s: %s", col, op, val, e)
    return df


def generate_report(summary: Dict[str, Any], execution_time: float,
                    records: List[Dict[str, Any]],
                    json_file: bool = False, txt_file: bool = False) -> None:
    """Generate report in JSON and/or TXT."""
    logger.info("Generating report...")
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - Merge & Filter Pipeline",
        "date": current_date,
        "execution_time_seconds": round(float(execution_time), 2),
        "summary": summary,
        "file_records": records,
        "notes": [
            "CSV files merged.",
            "Filters applied if provided.",
            "Fallback applied for errors."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False, default=str)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - Merge & Filter Pipeline\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Success: {summary.get('success', 0)}\n")
            tf.write(f"Failures: {summary.get('failures', 0)}\n")
            tf.write(f"Failed files: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n\n")
            tf.write("File Records:\n")
            for r in records:
                tf.write(f"- {r['name']}: Records: {r['records']} | Duplicates ignored: {r['duplicates_ignored']}\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(output_file: str, reports: List[str]) -> None:
    """Move results and logs to result folder."""
    logger.info("Moving results to 'result' folder...")
    log_type = os.path.exists("process_txt.log")
    log: List[str] = ["process_txt.log", "errors_txt.log"] if log_type else ["process_json.log", "errors_json.log"]

    destination = Path("result")
    destination.mkdir(exist_ok=True)

    files: List[str] = [output_file] + reports + log

    for file in files:
        if file and os.path.exists(file):
            target = destination / os.path.basename(file)
            if target.exists():
                if target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
            shutil.move(file, target)
            logger.info("File moved: %s", file)



def main() -> None:
    global logger

    parser = argparse.ArgumentParser()
    parser.add_argument("--files_csv", nargs="+", required=True, help="CSV files to process")
    parser.add_argument("--output_csv", default="output.csv", help="Final CSV file name")
    parser.add_argument("--filter", action="store_true", help="Apply filter if filter.json exists")
    parser.add_argument("--for_NaN", default="Not Informed", help="Replacement string for missing values")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    handlers: List[Handler] = []
    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="Merge & Filter Pipeline")
        logger.info("Logger initialized in JSON mode.")
    else:
        logger, handlers = logging_txt()
        logger.info("Logger initialized in TXT mode.")

    start_time = time.time()
    logger.info("Starting Merge & Filter Pipeline...")

    args.files_csv = [f if f.lower().endswith(".csv") else f + ".csv" for f in args.files_csv]
    args.output_csv = args.output_csv if args.output_csv.lower().endswith(".csv") else args.output_csv + ".csv"
    logger.debug("Files to process: %s", args.files_csv)

    files_validated = open_input(args.files_csv)
    if files_validated["status"] == "OK":
        logger.info("File validation successful. %d file(s) ready for processing.", len(files_validated["files"]))

        processed = clean_and_merge(files_validated["files"], null_replacement=args.for_NaN)
        df = processed["df"]

        if args.filter:
            try:
                with open("filter.json", "r", encoding="utf-8") as f:
                    filters = json.load(f)["filters"]
                df = apply_filter(df, filters)
                logger.info("Filters applied successfully.")
            except Exception as e:
                logger.warning("Could not apply filters: %s", e)

        df.to_csv(args.output_csv, index=False)
        logger.info("Final CSV generated: %s", args.output_csv)

        summary = {
            "success": int(len(files_validated["files"])),
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
        args.output_csv = "output.csv"

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
    save_results(args.output_csv, reports)
    print("Pipeline completed successfully.")



if __name__ == "__main__":
    main()