#!/usr/bin/env python3
"""
TripWise AI - Kaggle Data Schema Inspector & Importer

This utility inspects the actual files downloaded in the repository, validates their
schema without assumptions, and safely imports verified destinations and attractions
into SQLite.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app.database import engine, Base, SessionLocal
from backend.app.services.data_importer import inspect_dataset_files, import_kaggle_tourism_dataset

def main():
    print("=" * 70)
    print("TripWise AI: Kaggle Dataset Inspector & Importer")
    print("=" * 70)

    print("\n[Step 1] Inspecting local dataset files...")
    report = inspect_dataset_files(".")
    
    for filename, info in report.items():
        print(f"\n* File: {filename}")
        if info.get("exists"):
            print(f"  - Status: {info.get('status', 'Found')}")
            print(f"  - Records: {info.get('record_count', 'N/A')}")
            if "columns" in info:
                print(f"  - Verified Columns: {info['columns']}")
            if "sample_keys" in info:
                print(f"  - Sample Top Keys: {info['sample_keys']}")
        else:
            print("  - Status: Not present in working directory")

    print("\n" + "-" * 70)
    print("[Step 2] Importing verified Kaggle destinations into SQLite...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        count = import_kaggle_tourism_dataset(db, ".")
        print(f"\nImport Completed Successfully!")
        print(f"Total destinations imported/active: {count}")
        print("All records have been visibly tagged with their source and status.")
    except Exception as e:
        print(f"\nImport encountered error: {e}")
    finally:
        db.close()

    print("=" * 70)

if __name__ == "__main__":
    main()
