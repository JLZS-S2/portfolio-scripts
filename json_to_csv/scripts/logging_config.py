import os
import logging
import logging.config
import json

def setup_logging(config_file="logging_config.json", logger_name="JSON to CSV Automation"):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    return logging.getLogger(logger_name)