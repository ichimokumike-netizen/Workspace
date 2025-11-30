"""
Script: validate_pdf_quality.py
Purpose: Validate PDF meets tier requirements BEFORE finalizing
Inputs: PDF file path, tier (tier1/tier2/tier3)
Outputs: Validation result (pass/fail) with specific metrics
Author: AI-Assisted
Created: 2025-11-29

TIER REQUIREMENTS:
- Tier 1: 20-25 pages minimum, $17 price point
- Tier 2: 30-60 pages minimum, $27-$47 price point
- Tier 3: 60+ pages minimum, $47-$97 price point
"""

import os
import sys
from PyPDF2 import PdfReader


# Tier requirements (minimum pages)
TIER_REQUIREMENTS = {
    "tier1": {
        "min_pages": 20,
        "max_pages": 25,
        "target_pages": 25,
        "price": "$17"
    },
    "tier2": {
        "min_pages": 30,
        "max_pages": 60,
        "target_pages": 45,
        "price": "$27-$47"
    },
    "tier3": {
        "min_pages": 60,
        "max_pages": 100,
        "target_pages": 80,
        "price": "$47-$97"
    }
}


def validate_pdf(pdf_path, tier="tier1"):
    """
    Validate PDF meets tier requirements.

    Returns:
        dict: Validation result with metrics
    """
    if not os.path.exists(pdf_path):
        return {
            "valid": False,
            "error": f"PDF file not found: {pdf_path}"
        }

    # Get tier requirements
    requirements = TIER_REQUIREMENTS.get(tier)
    if not requirements:
        return {
            "valid": False,
            "error": f"Invalid tier: {tier}. Must be tier1, tier2, or tier3"
        }

    # Read PDF
    try:
        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
        file_size_kb = os.path.getsize(pdf_path) / 1024

        # Check page count
        min_pages = requirements["min_pages"]
        max_pages = requirements["max_pages"]

        is_valid = min_pages <= page_count <= max_pages

        result = {
            "valid": is_valid,
            "tier": tier,
            "page_count": page_count,
            "min_required": min_pages,
            "max_allowed": max_pages,
            "target_pages": requirements["target_pages"],
            "file_size_kb": round(file_size_kb, 1),
            "price_point": requirements["price"],
            "pdf_path": pdf_path
        }

        # Add error message if invalid
        if not is_valid:
            if page_count < min_pages:
                result["error"] = f"PDF too short: {page_count} pages (need {min_pages}+ for {tier})"
                result["pages_needed"] = min_pages - page_count
            else:
                result["error"] = f"PDF too long: {page_count} pages (max {max_pages} for {tier})"
                result["pages_over"] = page_count - max_pages

        return result

    except Exception as e:
        return {
            "valid": False,
            "error": f"Error reading PDF: {str(e)}"
        }


def print_validation_result(result):
    """Print validation result in a readable format."""
    print("\n" + "="*80)
    print(">>> PDF QUALITY VALIDATION")
    print("="*80)

    if "error" in result and not result.get("valid"):
        print(f"\n[FAILED] {result['error']}")
        if "pages_needed" in result:
            print(f"[ACTION] Add {result['pages_needed']} more pages to meet {result['tier']} requirements")
        return

    print(f"\nTier: {result['tier'].upper()}")
    print(f"PDF: {result['pdf_path']}")
    print(f"Pages: {result['page_count']} (target: {result['target_pages']}, min: {result['min_required']})")
    print(f"File Size: {result['file_size_kb']} KB")
    print(f"Price Point: {result['price_point']}")

    if result["valid"]:
        print(f"\n[SUCCESS] PDF meets {result['tier']} quality requirements!")
        print(f"[READY] Upload to Gumroad/Etsy at {result['price_point']}")
    else:
        print(f"\n[FAILED] {result['error']}")
        if "pages_needed" in result:
            print(f"[ACTION] Add {result['pages_needed']} more pages")
        elif "pages_over" in result:
            print(f"[ACTION] Consider upgrading to tier2 or trim {result['pages_over']} pages")

    print("="*80)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_pdf_quality.py <pdf_file> [tier]")
        print("\nExample:")
        print("  python validate_pdf_quality.py deliverables/my-guide.pdf tier1")
        print("\nTiers:")
        print("  tier1 = 20-25 pages ($17)")
        print("  tier2 = 30-60 pages ($27-$47)")
        print("  tier3 = 60+ pages ($47-$97)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    tier = sys.argv[2] if len(sys.argv) > 2 else "tier1"

    result = validate_pdf(pdf_path, tier)
    print_validation_result(result)

    # Exit with error code if validation failed
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
