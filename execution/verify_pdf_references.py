"""
Script: verify_pdf_references.py
Purpose: Verify that a PDF includes properly formatted References section
Inputs: PDF file path
Outputs: Validation report
Author: AI-Assisted
Created: 2025-11-29
"""

import sys
from PyPDF2 import PdfReader


def verify_references(pdf_path):
    """Check if PDF contains References section"""

    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        # Search last 5 pages for "References" section
        has_references = False
        references_page = None

        for i in range(max(0, total_pages - 5), total_pages):
            text = reader.pages[i].extract_text().lower()
            # Look for references keyword in various formats
            if any(keyword in text for keyword in ["references", "bibliography", "sources", "works cited"]):
                has_references = True
                references_page = i + 1
                break

        print(f"\n{'='*80}")
        print(f">>> PDF REFERENCES VERIFICATION")
        print(f"{'='*80}")
        print(f"File: {pdf_path}")
        print(f"Total Pages: {total_pages}")

        if has_references:
            print(f"References Section: FOUND (page {references_page})")
            print(f"Status: PASS")
        else:
            print(f"References Section: NOT FOUND")
            print(f"Status: FAIL - Missing required References section")

        print(f"{'='*80}\n")

        return has_references

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_pdf_references.py <pdf_file>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    has_refs = verify_references(pdf_path)

    sys.exit(0 if has_refs else 1)


if __name__ == "__main__":
    main()
