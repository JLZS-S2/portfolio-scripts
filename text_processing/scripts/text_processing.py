import os
import re
import shutil
import json
import argparse
import time
import chardet
from typing import Dict, Any, List
from logging import Logger, Handler
from logging_config import setup_logging
from logging_txt import logging_txt
from datetime import datetime
import logging

logger: Logger | None = None


def clean_text(files: List[str]) -> Dict[str, Any]:
    """Remove blank lines and generate new files prefixed with 'new_'."""
    logger.info("Starting cleaning process for %d file(s)", len(files))
    all_info: List[str] = []
    failed_list: List[str] = []
    failures: int = 0

    for file in files:
        logger.debug("Processing file: %s", file)
        try:
            with open(file, "rb") as f:
                raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding: str | None = result.get("encoding")
            logger.debug("Detected encoding for %s: %s", file, encoding)

            with open(file, "r", encoding=encoding) as f:
                text = f.read()
            cleaned_text = re.sub(r"\n\s*\n", "\n", text)
            new_file = "new_" + os.path.basename(file)
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
                all_info.append(new_file)
            logger.info("File %s cleaned successfully → %s", file, new_file)
        except Exception as e:
            logger.error("Error processing %s: %s", file, e)
            failures += 1
            failed_list.append(file)
            continue

    logger.info("Cleaning completed: %d success(es), %d failure(s)", len(all_info), failures)

    if failures == len(files):
        logger.critical("All files failed.")
        return {"status": "ERROR", "files": [], "failures": failures, "failed_list": failed_list}

    if failures > 0:
        logger.warning("Files not processed: %s", failed_list)

    return {"status": "OK", "files": all_info, "failures": failures, "failed_list": failed_list}


def split_keywords(keywords: List[str], files: List[str]) -> List[str]:
    """Split text using multiple keywords."""
    logger.info("Splitting files using keywords: %s", keywords)
    keyword = "|".join(re.escape(k) for k in keywords)
    split_files: List[str] = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            parts = [part.strip() for part in re.split(keyword, text) if part.strip()]

        with open(file, "w", encoding="utf-8") as f:
            f.write("\n".join(parts))

        split_files.append(file)
        logger.info("Keywords '%s' applied to file %s", keyword, file)

    logger.info("Keyword splitting completed for %d file(s)", len(split_files))
    return split_files


def count_lines_words(files: List[str]) -> Dict[str, Dict[str, int]]:
    """Count lines and words in each file."""
    logger.info("Starting line and word count for %d file(s)", len(files))
    all_info: Dict[str, Dict[str, int]] = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            lines = text.splitlines()
            words = re.findall(r"\b\w+\b", text)
            all_info[file] = {"lines": len(lines), "words": len(words)}
        logger.info("Count completed for %s: %s lines, %s words", file, len(lines), len(words))
    return all_info


def generate_report(report_data: Dict[str, Dict[str, int]], summary: Dict[str, Any],
                    execution_time: float, json_file: bool = False, txt_file: bool = False) -> None:
    """Generate report in JSON and/or TXT."""
    logger.info("Generating report...")
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    final_report: Dict[str, Any] = {
        "report_title": "Report - Text Processing Automation",
        "date": current_date,
        "execution_time_seconds": round(execution_time, 2),
        "files": report_data,
        "summary": summary,
        "notes": [
            "All files were cleaned and split by keyword.",
            "Reports generated in JSON and TXT formats.",
            "Files moved to organized folders.",
            "Fallback applied for errors."
        ]
    }

    if json_file:
        with open("report.json", "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False)
        logger.info("JSON report generated.")

    if txt_file or (not json_file and not txt_file):
        with open("report.txt", "w", encoding="utf-8") as tf:
            tf.write("Report - Text Processing Automation\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Summary of processed files:\n")
            for file, stats in report_data.items():
                tf.write(f"- {file}: {stats['lines']} lines, {stats['words']} words\n")
            tf.write("\nExecution Summary:\n")
            tf.write(f"Files processed successfully: {summary.get('success', 0)}\n")
            tf.write(f"Files failed: {summary.get('failures', 0)}\n")
            tf.write(f"Failed files: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated.")


def save_results(files: List[str], reports: List[str]) -> None:
    """Move processed files and reports into organized folders."""
    logger.info("Moving results to 'result' folder...")
    if os.path.exists("process_json.log"):
        log: List[str] = ["process_json.log", "errors_json.log"]
    elif os.path.exists("process_txt.log"):
        log: List[str] = ["process_txt.log", "errors_txt.log"]
    else:
        log: List[str] = []

    destination = "result"
    subfolder = os.path.join(destination, "cleaned_files")
    os.makedirs(destination, exist_ok=True)
    os.makedirs(subfolder, exist_ok=True)

    for report in reports + log:
        if os.path.exists(report):
            shutil.move(report, os.path.join(destination, os.path.basename(report)))
            logger.info("Report/log moved: %s", report)

    for file in files:
        if os.path.exists(file):
            shutil.move(file, os.path.join(subfolder, os.path.basename(file)))
            logger.info("File moved: %s", file)

    print("- All results have been moved.")


def main() -> None:
    global logger

    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, nargs="+", help="TXT files to process")
    parser.add_argument("--keywords", required=True, nargs="+", help="Keywords for splitting")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    handlers: List[Handler] = []
    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="Text Processing Automation")
        logger.info("Logger initialized in JSON mode.")
    else:
        logger, handlers = logging_txt()
        logger.info("Logger initialized in TXT mode.")

    args.file = [f if f.endswith(".txt") else f + ".txt" for f in args.file]
    logger.debug("Files to process: %s", args.file)
    logger.debug("Keywords to apply: %s", args.keywords)

    formatted_files = clean_text(args.file)
    if formatted_files["status"] == "OK":
        processed_files = split_keywords(args.keywords, formatted_files["files"])
        stats = count_lines_words(processed_files)
        summary = {
            "success": len(processed_files),
            "failures": formatted_files["failures"],
            "failed_list": formatted_files["failed_list"]
        }
    else:
        stats = {}
        summary = {
            "success": 0,
            "failures": formatted_files.get("failures", len(args.file)),
            "failed_list": formatted_files.get("failed_list", args.file)
        }

    execution_time = time.time() - start_time
    logger.info("Pipeline execution finished in %.2f seconds.", execution_time)
    generate_report(stats, summary, execution_time, json_file=args.json, txt_file=args.txt)

    reports: List[str] = []
    if args.json and args.txt:
        reports = ["report.json", "report.txt"]
    elif args.json:
        reports = ["report.json"]
    else:
        reports = ["report.txt"]

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

    files_to_move = list(stats.keys()) if stats else []
    save_results(files_to_move, reports)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

