# ICT Framework

Demonstration ICT framework for the SPEA 3030 tester, built for SPEA_3030.

## Overview
A thin but complete automation stack covering test sequencing, fixture control, 
result logging, and a thread-safe Tkinter operator GUI.

## Project Structure
- `controllers/` — abstract base class and SPEA 3030 implementation
- `core/` — test sequencing, result logging, barcode reader, fixture control
- `ui/` — Tkinter operator GUI
- `main_gui.py` — application entry point
- `testplan.xml` — declarative test plan

## Requirements
Python 3.9 or later. No third-party packages required.

## Usage
python main_gui.py
MIT License
