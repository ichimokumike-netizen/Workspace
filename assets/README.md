# Assets Folder

This folder contains reusable assets for PDF generation and branding.

## Files

### `author_bio.md`
**Purpose:** Standard author biography that appears in all PDF guides

**Usage:**
- This file is automatically loaded by PDF generation scripts
- To update the author bio across ALL PDFs, simply edit this file
- Changes apply immediately to all future PDF generations
- No need to modify any code - just edit this markdown file

**Format:** Markdown format with image reference and text

**Used by:**
- `execution/generate_tier1_instant.py`
- Any future PDF generation scripts

### `founder_headshot.png`
**Purpose:** Author profile photo that appears in the "About the Author" section

**Referenced by:** `author_bio.md`

---

## For AI Agents

When generating PDFs or creating marketing materials:

1. **Author Bio:** Read from `assets/author_bio.md` - this is the canonical source
2. **Author Photo:** Use `assets/founder_headshot.png`
3. **Never hardcode bio text** - always read from the file to ensure consistency

## Updating the Author Bio

Simply edit `author_bio.md` - no code changes needed. All PDF generation scripts will automatically use the updated content.
