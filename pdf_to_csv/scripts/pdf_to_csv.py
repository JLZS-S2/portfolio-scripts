import os
import shutil
import argparse
import pandas as pd
import time
import pdfplumber
import csv
from io import StringIO
from datetime import datetime
from typing import Dict, Any, List
from logging import Logger, Handler
from logging_config import setup_logging
from logging_txt import logging_txt

from pypdf import PdfReader
from pypdf.errors import WrongPasswordError
import logging

logger: Logger | None = None


def open_pdfs(files: List[str]) -> Dict[str, Any]:
    """
    Validate PDF files using PdfReader only for error detection.
    Returns list of valid file paths.
    """
    logger.info("Starting validation of %d PDF files", len(files))
    success_list: List[str] = []
    failed_list: List[str] = []
    failures = 0

    for file in files:
        try:
            PdfReader(file)
            success_list.append(file)
            logger.info("File successfully validated: %s", file)

        except FileNotFoundError:
            failures += 1
            logger.error("File not found: %s", file)
            failed_list.append(file)
        except PermissionError:
            failures += 1
            logger.error("Permission denied: %s", file)
            failed_list.append(file)
        except WrongPasswordError:
            failures += 1
            logger.error("PDF protected by password: %s", file)
            failed_list.append(file)
        except Exception as e:
            failures += 1
            logger.error("Unexpected error in %s: %s", file, e)
            failed_list.append(file)

    logger.info("Validation completed: %d success(es), %d failure(s)", len(success_list), failures)

    if failures == len(files):
        logger.critical("All files failed.")
        return {"status": "ERROR", "files": [], "failures": failures, "failed_list": failed_list}

    return {"status": "OK", "files": success_list, "failures": failures, "failed_list": failed_list}


def parse_text_block(text: str) -> List[Dict[str, Any]]:
    """
    Detects separator automatically and converts text into list of dicts.
    """
    lines = text.strip().split("\n")
    if len(lines) <= 1:
        return []

    sample = "\n".join(lines)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t ")
        logger.debug("Separator automatically detected: %s", dialect.delimiter)
    except csv.Error:
        dialect = csv.get_dialect("excel")
        logger.warning("Could not detect separator, using comma as default.")

    reader = csv.reader(StringIO(sample), dialect)
    rows = list(reader)

    header = [col.strip() for col in rows[0]]
    data = rows[1:]
    logger.debug("Header detected: %s", header)
    return [dict(zip(header, [col.strip() for col in row]))
            for row in data if len(row) == len(header)]


def type_identification(files: List[str]) -> Dict[str, Any]:
    """
    Extract tables OR text from PDFs, with automatic separator detection for text.
    """
    extracted_data: List[Dict[str, Any]] = []

    for file in files:
        logger.info("Processing file: %s", file)
        start_file = time.time()
        tables_count, text_count = 0, 0

        with pdfplumber.open(file) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                table = page.extract_table()
                if table:
                    tables_count += 1
                    header = table[0]
                    data = table[1:]
                    list_dicts = [dict(zip(header, row)) for row in data if len(row) == len(header)]
                    extracted_data.extend(list_dicts)
                    logger.debug("Page %d: extracted table (%d rows)", page_num, len(list_dicts))
                else:
                    text = page.extract_text() or ""
                    list_dicts = parse_text_block(text)
                    if list_dicts:
                        text_count += 1
                        extracted_data.extend(list_dicts)
                        logger.debug("Page %d: extracted text (%d lines)", page_num, len(list_dicts))

        logger.info("Summary of file %s: %d pages, %d with tables, %d with text. Time: %.2fs",
                    file, len(pdf.pages), tables_count, text_count, time.time() - start_file)

    logger.info("Extraction completed. Total records: %d", len(extracted_data))
    return {"all_data": extracted_data}


def null_values(df: pd.DataFrame, null_replacement: str) -> pd.DataFrame:
    """
    Replace null values in DataFrame.
    """
    if df.isna().any().any():
        null_cols = df.columns[df.isna().any()].tolist()
        logger.warning("Null values detected in the columns: %s", null_cols)
        df = df.fillna(null_replacement)
        logger.info("Null values replaced by '%s'", null_replacement)
    else:
        logger.info("No null value detected.")
    return df


def generate_report(summary: Dict[str, Any], execution_time: float,
                    records: List[Dict[str, Any]],
                    json_file: bool = False, txt_file: bool = False) -> None:
    """
    Generate report in JSON and/or TXT format.
    """
    import json
    logger.info("Generating report...")
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - PDF to CSV",
        "date": current_date,
        "execution_time_seconds": round(execution_time, 2),
        "summary": summary,
        "file_records": records,
        "notes": [
            "PDF extracted into CSV.",
            "Tables and text processed.",
            "Null values handled."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - PDF to CSV\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Success: {summary.get('success', 0)}\n")
            tf.write(f"Failures: {summary.get('failures', 0)}\n")
            tf.write(f"Failed files: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n\n")
            tf.write("File Records:\n")
            for r in records:
                tf.write(f"- {r['name']}: Records inserted: {r['records_inserted']}\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(output_files: List[str], reports: List[str]) -> None:
    """
    Move generated CSVs, reports, and logs into the 'result' folder.
    """
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
    """
    Main entry point.
    """
    global logger

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="PDF files to process")
    parser.add_argument("--output", default="output.csv", help="Output CSV filename")
    parser.add_argument("--for_NaN", default="Not Informed", help="Replacement for missing values")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    handlers: List[Handler] = []
    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="PDF Converter Pipeline")
        logger.info("Logger initialized in JSON mode.")
    else:
        logger, handlers = logging_txt()
        logger.info("Logger initialized in TXT mode.")

    start_time = time.time()
    logger.info("Starting PDF to CSV conversion pipeline...")

    # Normalize file names
    args.files = [f if f.lower().endswith(".pdf") else f + ".pdf" for f in args.files]
    logger.debug("Files to process: %s", args.files)

    # Validate files
    valid_files = open_pdfs(args.files)
    if valid_files["status"] == "OK":
        logger.info("File validation successful. %d file(s) ready for processing.", len(valid_files["files"]))

        # Extract tables/text
        text_files = type_identification(valid_files["files"])
        logger.info("Extraction completed. %d records obtained.", len(text_files["all_data"]))

        # Convert to DataFrame
        df = pd.DataFrame(text_files["all_data"])
        logger.debug("Initial DataFrame created with %d rows and %d columns.", len(df), len(df.columns))

        # Handle null values
        df_final = null_values(df, args.for_NaN)
        logger.info("Null value handling completed.")

        # Save CSV
        df_final.to_csv(args.output, index=False)
        logger.info("CSV file saved: %s", args.output)

        summary = {
            "success": len(valid_files["files"]),
            "failures": valid_files["failures"],
            "failed_list": valid_files["failed_list"]
        }
        records = [{"name": args.output, "records_inserted": len(df_final)}]
        output_files = [args.output]
    else:
        logger.error("File validation failed. No files processed.")
        summary = {
            "success": 0,
            "failures": valid_files["failures"],
            "failed_list": valid_files["failed_list"]
        }
        records = []
        output_files = []

    execution_time = time.time() - start_time
    logger.info("Pipeline execution finished in %.2f seconds.", execution_time)
    generate_report(summary, execution_time, records=records, json_file=args.json, txt_file=args.txt)

    reports = []
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
