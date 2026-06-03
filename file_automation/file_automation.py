import sys
import os
import shutil
import zipfile
import argparse
import json
import time
from datetime import datetime
from collections import Counter
from typing import Dict, Any, List

import logging
from logging.handlers import RotatingFileHandler
from logging import Logger, Handler

from logging_config import setup_logging
from logging_txt import logging_txt


logger: Logger | None = None


def organizer(mapping: Dict[str, str], folder_original: str, folder_organized: str,
              unmapped_folder: str = "OTHERS", move: bool = False, copy: bool = False) -> Dict[str, Any]:
    """Organize files from the original folder into subfolders based on their extensions."""
    try:
        logger.info("Starting organization of folder: %s", folder_original)
        for file in os.listdir(folder_original):
            ext = os.path.splitext(file)[1].lower().strip(".") or "no_extension"
            if ext in mapping:
                folder_destination = os.path.join(folder_organized, mapping[ext])
                os.makedirs(folder_destination, exist_ok=True)
                src = os.path.join(folder_original, file)
                dst = os.path.join(folder_destination, file)
                if move:
                    shutil.move(src, dst)
                    logger.debug("File %s moved to %s", file, folder_destination)
                else:
                    shutil.copy(src, dst)
                    logger.debug("File %s copied to %s", file, folder_destination)
            else:
                logger.warning("Unmapped extension: %s", ext)
                folder_extra = os.path.join(folder_organized, unmapped_folder, ext)
                os.makedirs(folder_extra, exist_ok=True)
                src = os.path.join(folder_original, file)
                dst = os.path.join(folder_extra, file)
                if move:
                    shutil.move(src, dst)
                    logger.debug("File %s moved to %s", file, folder_extra)
                else:
                    shutil.copy(src, dst)
                    logger.debug("File %s copied to %s", file, folder_extra)
        logger.info("Organization completed successfully")
        return {"status": "OK"}
    except FileNotFoundError:
        logger.error("Error: folder %s not found", folder_original)
        return {"status": "ERROR", "message": "Folder not found"}
    except Exception as e:
        logger.critical("Unexpected error during organization: %s", e)
        return {"status": "ERROR", "message": str(e)}


def counter(folder_organized: str) -> Dict[str, int]:
    """Count files by extension in organized folder."""
    counter_logger = logging.getLogger("CounterLogger")
    if not counter_logger.handlers:
        log_path = os.path.join(folder_organized, "counter.log")
        counter_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=2)
        counter_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        counter_logger.addHandler(counter_handler)
    counter_logger.setLevel(logging.INFO)

    logger.info("Starting file count in %s", folder_organized)
    extensions: List[str] = []
    for root, dirs, files in os.walk(folder_organized):
        for f in files:
            ext = os.path.splitext(f)[1].lower().strip(".") or "no_extension"
            extensions.append(ext)

    count = Counter(extensions)
    for ext, qty in count.items():
        logger.info("Extension %s: %d files", ext, qty)
        counter_logger.info("%s: %d files", ext, qty)

    logger.info("Counting completed")
    for h in counter_logger.handlers[:]:
        h.flush()
        h.close()
        counter_logger.removeHandler(h)
    return dict(count)


def zip_folder(folder_organized: str) -> None:
    """Compress organized folder into a ZIP archive."""
    logger.info("Starting compression of folder: %s", folder_organized)
    zip_file = folder_organized + ".zip"
    try:
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for folder, subfolder, files in os.walk(folder_organized):
                for file in files:
                    path = os.path.join(folder, file)
                    zipf.write(path, os.path.relpath(path, folder_organized))
                    logger.debug("File %s added to ZIP", path)
        logger.info("Compression completed successfully: %s", zip_file)
    except Exception as e:
        logger.error("Error during compression: %s", e)


def generate_report(summary: Dict[str, Any], execution_time: float,
                    counts: Dict[str, int] | None = None,
                    json_file: bool = False, txt_file: bool = False,
                    folder_organized: str = "Organized files") -> None:
    """Generate report in JSON and/or TXT."""
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_report: Dict[str, Any] = {
        "report_title": "Report - File Organizer Pipeline",
        "date": current_date,
        "execution_time_seconds": round(execution_time, 2),
        "summary": summary,
        "file_counts": counts if counts else {},
        "notes": [
            "Files organized by extension.",
            "Files counted by extension.",
            "Organized folder compressed into ZIP.",
            "Fallback applied for errors."
        ]
    }

    if json_file:
        json_path = os.path.join(folder_organized, "report.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(final_report, jf, indent=4, ensure_ascii=False)
        logger.info("JSON report generated at %s", json_path)

    if txt_file or (not json_file and not txt_file):
        txt_path = os.path.join(folder_organized, "report.txt")
        with open(txt_path, "w", encoding="utf-8") as tf:
            tf.write("Report - File Organizer Pipeline\n")
            tf.write(f"Date: {current_date}\n")
            tf.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            tf.write("Execution Summary:\n")
            tf.write(f"Success: {summary.get('success', 0)}\n")
            tf.write(f"Failures: {summary.get('failures', 0)}\n")
            tf.write(f"Failed items: {', '.join(summary.get('failed_list', [])) if summary.get('failed_list') else 'None'}\n\n")
            tf.write("File Counts:\n")
            if counts:
                for ext, qty in counts.items():
                    tf.write(f"- {ext}: {qty} files\n")
            else:
                tf.write("No files counted.\n")
            tf.write("\nNotes:\n")
            for note in final_report["notes"]:
                tf.write(f"- {note}\n")
        logger.info("TXT report generated at %s", txt_path)


def save_results(output_files: List[str], reports: List[str]) -> None:
    """Move results, logs, and organized folder to result directory."""
    log_type = os.path.exists("process_txt.log")
    log: List[str] = ["process_txt.log", "errors_txt.log"] if log_type else ["process_json.log", "errors_json.log"]

    destination = os.path.join("result")
    os.makedirs(destination, exist_ok=True)

    files: List[str] = output_files + reports + log

    # Move files
    for file in files:
        if file and os.path.exists(file):
            shutil.move(file, os.path.join(destination, file))

    # Move the entire organized folder
    organized_folder = "Organized files"
    if os.path.exists(organized_folder):
        target_path = os.path.join(destination, organized_folder)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.move(organized_folder, target_path)
        logger.info("Organized folder moved to result directory.")


def main() -> None:
    start_time: float = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_original", required=True, help="Folder containing all files")
    parser.add_argument("--folder_organized", default="Organized files", help="Folder where organized subfolders will be created")
    parser.add_argument("--move_files", action="store_true", help="Move the files to organized folder")
    parser.add_argument("--copy_files", action="store_true", help="Copy the files to organized folder")
    parser.add_argument("--extensions", nargs="+", metavar="EXT:FOLDER", help="Extensions mapping")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--txt", action="store_true", help="Generate TXT report")
    parser.add_argument("--log_json", action="store_true", help="Generate JSON log")
    parser.add_argument("--log_txt", action="store_true", help="Generate TXT log")
    args = parser.parse_args()

    global logger
    handlers: List[Handler] = []

    if args.log_json and not args.log_txt:
        logger = setup_logging(logger_name="File Organizer Pipeline")
    else:
        logger, handlers = logging_txt()

    try:
        if args.extensions:
            mapping = {item.split(":")[0]: item.split(":")[1] for item in args.extensions}
            with open("extension.json", "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=4)
        else:
            with open("extension.json", "r", encoding="utf-8") as f:
                mapping = json.load(f)
    except Exception as e:
        logger.error("Error loading extension mapping: %s", e)
        summary = {"success": 0, "failures": 1, "failed_list": ["extension.json"]}
        execution_time = time.time() - start_time
        os.makedirs(args.folder_organized, exist_ok=True)
        generate_report(summary, execution_time, counts=None, json_file=args.json, txt_file=args.txt, folder_organized=args.folder_organized)
        for handler in handlers[:]:
            handler.flush()
            handler.close()
            logger.removeHandler(handler)
        save_results([], ["report.json" if args.json else "report.txt"])
        sys.exit(1)

    logger.info("Execution started")
    result = organizer(mapping, args.folder_original, args.folder_organized, move=args.move_files, copy=args.copy_files)

    if result["status"] == "OK":
        counts = counter(args.folder_organized)
        zip_folder(args.folder_organized)
        summary = {"success": 1, "failures": 0, "failed_list": []}
    else:
        logger.error("Process interrupted: %s", result["message"])
        counts = None
        summary = {"success": 0, "failures": 1, "failed_list": [args.folder_original]}

    execution_time = time.time() - start_time
    generate_report(summary, execution_time, counts=counts, json_file=args.json, txt_file=args.txt, folder_organized=args.folder_organized)

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

    output_files = [args.folder_organized + ".zip"]
    save_results(output_files, reports)

    logger.info("Execution finished")


if __name__ == "__main__":
    main()