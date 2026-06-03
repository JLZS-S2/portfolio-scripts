import logging
import logging.config
import json

def setup_logging(config_file="logging_config.json", logger_name="JSON to CSV Automation"):
    with open(config_file, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    return logging.getLogger(logger_name)