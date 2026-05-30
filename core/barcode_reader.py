# core/barcode_reader.py

def read_barcode() -> str:
    # Simplest version: prompt operator
    barcode = input("Scan or enter serial number: ").strip()
    return barcode
