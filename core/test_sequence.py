# core/test_sequence.py

from typing import List, Dict
from controllers.base_controller import ICTControllerBase
from .result_logger import ResultLogger

class TestSequence:
    def __init__(self, controller: ICTControllerBase, logger: ResultLogger):
        self.controller = controller
        self.logger = logger

    def run_sequence(self, serial: str, tests: List[Dict]) -> list[dict]:
        """
        tests: list of dicts like:
        {
            "name": "POWER_ON",
            "critical": True
        }
        """
        results = []
        self.logger.log_info(f"=== Starting ICT for SN={serial} ===")

        for t in tests:
            name = t["name"]
            critical = t.get("critical", False)

            self.logger.log_info(f"Running test: {name}")
            result = self.controller.run_test(name)
            results.append(result)

            if result["status"] != "PASS":
                self.logger.log_failure(name, result.get("details", ""))
                if critical:
                    self.logger.log_info(
                        f"Critical test {name} failed. Aborting remaining tests."
                    )
                    break

        self.logger.log_summary(serial, results)
        return results
