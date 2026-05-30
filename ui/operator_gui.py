# ui/operator_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import queue

class OperatorGUI:
    def __init__(self, root, controller, test_sequence, load_tests_func):
        self.root = root
        self.controller = controller
        self.test_sequence = test_sequence
        self.load_tests = load_tests_func
        self._queue = queue.Queue()          # ← shared message channel

        self.root.title("SPEA 3030 ICT System")
        self.root.geometry("600x500")
        
        # Serial number entry        # Serial number entry
        self.serial_label = ttk.Label(root, text="Serial Number:")
        self.serial_label.pack(pady=5)

        self.serial_entry = ttk.Entry(root, width=40)
        self.serial_entry.pack(pady=5)

        # Start button
        self.start_button = ttk.Button(root, text="Start Test",
                                       command=self.start_test_thread)
        self.start_button.pack(pady=10)

        # Results display
        self.results_box = tk.Text(root, height=20, width=70, state="disabled")
        self.results_box.pack(pady=10)

        # PASS/FAIL banner
        self.status_label = ttk.Label(root, text="", font=("Arial", 18, "bold"))
        self.status_label.pack(pady=10)

        self._poll()                         # ← start the polling loop

    # ── queue polling (runs on main thread only) ─────────────────────────────

    def _poll(self):
        """Drain all pending messages from the worker and update the UI."""
        try:
            while True:                      # consume everything available
                msg = self._queue.get_nowait()
                self._handle(msg)
        except queue.Empty:
            pass
        finally:
            self.root.after(50, self._poll) # reschedule every 50 ms

    def _handle(self, msg):
        """Apply one message to the UI. Always called on the main thread."""
        kind = msg["kind"]
        if kind == "log":
            self.results_box.config(state="normal")
            self.results_box.insert("end", msg["text"] + "\n")
            self.results_box.see("end")
            self.results_box.config(state="disabled")
        elif kind == "status":
            color = "green" if msg["passed"] else "red"
            text  = "PASS"  if msg["passed"] else "FAIL"
            self.status_label.config(text=text, foreground=color)
        elif kind == "button":
            self.start_button.config(state=msg["state"])
        elif kind == "clear":
            self.results_box.config(state="normal")
            self.results_box.delete("1.0", "end")
            self.results_box.config(state="disabled")
            self.status_label.config(text="")

    # ── safe logging (can be called from any thread) ──────────────────────────

    def log(self, message):
        """Put a log message onto the queue; safe to call from worker thread."""
        self._queue.put({"kind": "log", "text": message})

    # ── test execution (worker thread) ───────────────────────────────────────

    def start_test_thread(self):
        serial = self.serial_entry.get().strip()
        if not serial:
            messagebox.showerror("Error", "Please enter a serial number.")
            return
        self.start_button.config(state="disabled")  # still on main thread here
        thread = Thread(target=self._run_test, args=(serial,), daemon=True)
        thread.start()

    def _run_test(self, serial):
        """Worker thread — never touches widgets directly."""
        self._queue.put({"kind": "clear"})
        self.log(f"=== Starting ICT for SN={serial} ===")

        self.log("Closing fixture...")
        self.controller.fixture_close()

        tests   = self.load_tests("testplan.xml")
        results = self.test_sequence.run_sequence(serial, tests)

        self.log("Opening fixture...")
        self.controller.fixture_open()

        passed = all(r["status"] == "PASS" for r in results)
        self._queue.put({"kind": "status", "passed": passed})
        self._queue.put({"kind": "button", "state": "normal"})