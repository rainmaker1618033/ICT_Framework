import tkinter as tk
import xml.etree.ElementTree as ET

from controllers.spea_3030 import SPEA3030Controller
from core.result_logger import ResultLogger
from core.test_sequence import TestSequence
from ui.operator_gui import OperatorGUI

def load_tests_from_xml(xml_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    tests = []
    for t in root.findall("test"):
        tests.append({
            "name": t.get("name"),
            "critical": t.get("critical", "false").lower() == "true"
        })
    return tests

def main():
    controller = SPEA3030Controller("testplan.xml")
    logger = ResultLogger()
    seq = TestSequence(controller, logger)

    controller.connect()
    controller.load_testplan("testplan.xml")

    root = tk.Tk()
    gui = OperatorGUI(root, controller, seq, load_tests_from_xml)
    root.mainloop()

    controller.disconnect()

if __name__ == "__main__":
    main()
