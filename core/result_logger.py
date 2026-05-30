# core/result_logger.py

import logging
from datetime import datetime
from pathlib import Path

class ResultLogger:
    def __init__(self, logfile: str = "ict_results.log"):
        self.logfile = Path(logfile)
        logging.basicConfig(
            filename=self.logfile,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def log_info(self, msg: str):
        print(msg)
        logging.info(msg)

    def log_failure(self, test_name: str, details: str = ""):
        msg = f"FAIL: {test_name} - {details}"
        print(msg)
        logging.error(msg)

    def log_summary(self, serial: str, results: list[dict]):
        passed = all(r["status"] == "PASS" for r in results)
        status = "PASS" if passed else "FAIL"
        logging.info(f"SUMMARY - SN={serial} - STATUS={status}")
