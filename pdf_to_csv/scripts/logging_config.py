import logging
import logging.config
import json
import os

def setup_logging(config_file="logging_config.json", logger_name="PDF Converter Pipeline"):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    return logging.getLogger(logger_name)