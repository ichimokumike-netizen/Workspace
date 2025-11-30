"""
Script: generate_pdf_simple.py
Purpose: Convert Markdown content to PDF (simple version for MVP)
Inputs: Markdown file path
Outputs: PDF file
Author: AI-Assisted
Created: 2025-11-29
"""

import os
import sys
from markdown_pdf import MarkdownPdf, Section
from datetime import datetime


def generate_pdf(markdown_file, output_file=None):
    """
    Convert Markdown file to PDF.

    Args:
        markdown_file: Path to markdown file
        output_file: Path for output PDF (optional)
    """
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate output filename if not provided
    if not output_file:
        base_name = os.path.splitext(os.path.basename(markdown_file))[0]
        output_file = f"deliverables/{base_name}.pdf"

    # Ensure deliverables directory exists
    os.makedirs('deliverables', exist_ok=True)

    print(f"[*] Converting {markdown_file} to PDF...")

    # Create PDF
    pdf = MarkdownPdf()
    pdf.add_section(Section(content))
    pdf.save(output_file)

    print(f"[+] PDF generated: {output_file}")

    # Get file size
    size_bytes = os.path.getsize(output_file)
    size_kb = size_bytes / 1024

    print(f"[+] File size: {size_kb:.1f} KB")

    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf_simple.py <markdown_file> [output_file]")
        print("\nExample:")
        print("  python generate_pdf_simple.py .tmp/chatgpt-guide-content.md")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(markdown_file):
        print(f"[X] Error: File not found: {markdown_file}")
        sys.exit(1)

    try:
        result = generate_pdf(markdown_file, output_file)
        print(f"\n[+] Success! Your PDF is ready to sell.")
        print(f"[+] Location: {result}")

    except Exception as e:
        print(f"[X] Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
