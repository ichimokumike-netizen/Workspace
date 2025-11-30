# PDF Product Research Automation

> Automated research system for high-volume PDF information products with Exploding Topics integration

## Goal

Generate comprehensive, data-driven research reports on PDF product opportunities for any niche. This directive automates the research process that would normally take 2-3 hours of manual work, producing actionable insights, template recommendations, and market analysis in minutes.

## Inputs
     - `--niche` (optional): Topic to research
     - `--output` (optional): Output directory (defaults to `.tmp/`)
   - **Output:** 
     - Markdown research report in `.tmp/pdf_research_[topic]_[timestamp].md`
     - JSON data file in `.tmp/pdf_research_[topic]_[timestamp].json`

## Process

### Quick Start (Automated Topic Selection):

```bash
# From workspace root
python execution/research_pdf_products.py
```

This will:
1. Load Exploding Topics data from `assets/`
2. Analyze trending topics for PDF product potential
3. Auto-select the highest-scoring topic
4. Generate comprehensive research report

### Research Specific Niche:

```bash
python execution/research_pdf_products.py --niche "ChatGPT productivity"
```

### Custom Output Directory:

```bash
python execution/research_pdf_products.py --niche "Notion templates" --output deliverables/
```

### Step-by-Step Workflow:

1. **Export Exploding Topics Data**
   - Log into your Exploding Topics account
   - Navigate to your saved searches or trending topics
   - Export as CSV or JSON
   - Save to `Workspace/assets/exploding_topics_[date].csv`

2. **Run Research Script**
   ```bash
   python execution/research_pdf_products.py --niche "your topic"
   ```

3. **Review Generated Report**
   - Open `.tmp/pdf_research_[topic]_[timestamp].md`
   - Review trending topics analysis
   - Note recommended search queries

4. **Execute Search Queries (AI Agent or Manual)**
   - Use the generated search queries to gather specific product examples
   - AI Agent can execute these via web search
   - Manual: Copy queries into Google, analyze results

5. **Refine & Iterate**
   - Based on findings, run script again with refined niche
   - Example: "AI tools" → "ChatGPT prompts for marketers"
   - Narrower niches = better product opportunities

## Outputs

### Primary Outputs:

- **Research Report** (`.tmp/pdf_research_[topic]_[timestamp].md`)
  - Executive summary with key findings
  - Exploding Topics trending data analysis
  - Prioritized search queries for deeper research
  - Product category analysis (6 major categories)
  - Pricing strategy guidelines
  - Template recommendations specific to your topic
  - Actionable next steps

- **Data File** (`.tmp/pdf_research_[topic]_[timestamp].json`)
  - Structured JSON for programmatic access
  - All research data in machine-readable format
  - Can be consumed by other scripts or AI agents

### Report Sections:

1. **Executive Summary** - High-level findings and metrics
2. **Exploding Topics Data** - Top 10 trending topics with growth indicators
3. **Recommended Research Queries** - Prioritized search queries (high/medium/low priority)
4. **Product Category Analysis** - Revenue potential for each category
5. **Pricing Strategy Guidelines** - Tier-based pricing recommendations
6. **Template Recommendations** - 5 specific templates for your niche with time/price estimates
7. **Next Steps** - Actionable checklist to move forward

## Edge Cases

### Issue 1: No Exploding Topics Data Found

- **Symptom**: Script runs but shows "⚠ No Exploding Topics data found"
- **Cause**: No CSV/JSON files in `assets/` folder with relevant keywords
- **Solution**: 
  1. Check filename contains "exploding", "trend", or "topic"
  2. Verify file is in `Workspace/assets/` directory
  3. Script will still run using fallback topic ("digital products")

### Issue 2: Empty or Invalid CSV Format

- **Symptom**: Script crashes when loading CSV
- **Cause**: CSV structure doesn't match expected format
- **Solution**:
  1. Ensure CSV has headers in first row
  2. Expected columns: `Topic`, `Growth`, `Volume` (or similar)
  3. Script is flexible - will adapt to different column names
  4. If issues persist, convert to JSON format

### Issue 3: Niche Too Broad or Too Narrow

- **Symptom**: Generated report feels generic or too limited
- **Cause**: Topic scope not optimized
- **Solution**:
  - **Too Broad**: "productivity" → "Notion productivity templates"
  - **Too Narrow**: "purple Notion budget tracker" → "budget tracking tools"
  - **Sweet Spot**: Specific enough for niche targeting, broad enough for market size

### Issue 4: Search Queries Not Producing Results

- **Symptom**: Manual searches return no relevant products
- **Cause**: Niche may not have established PDF product market yet
- **Solution**:
  - This is actually GOOD - low competition opportunity!
  - Pivot search to adjacent niches
  - Focus on "how to [topic]" searches to validate demand
  - Check if topic suits different digital product format (video course, tool, etc.)

## Performance Considerations

- **Expected Runtime:** ~5-15 seconds (without API calls)
  - Loading Exploding Topics data: 1-2 seconds
  - Analyzing trending topics: 2-5 seconds
  - Generating report: 2-5 seconds
  
- **With Google Search API:** ~30-60 seconds
  - Adds automated web search execution
  - Requires `GOOGLE_SEARCH_API_KEY` in `.env`

- **File Sizes:**
  - Markdown reports: ~10-30 KB
  - JSON data files: ~5-15 KB
  - Exploding Topics CSV: Varies (typically 50-500 KB)

- **API Calls:** 
  - None required (manual research mode)
  - Optional: Google Search API (6 queries per research run)

## Notes

### Best Practices:

1. **Read the Reference Guide First**
   - Review [`assets/exploding_topics_reference.md`](file:///C:/Users/t_bau/Workspace/assets/exploding_topics_reference.md) to understand indicators
   - Use the PDF Decision Matrix for quick decisions
   - Reference Channel Breakdown interpretation for marketing

2. **Regular Exploding Topics Updates**
   - Export new data weekly or monthly
   - Trends move fast - fresh data = better opportunities
   - Name files with date: `trends_2024-11-29.csv`

2. **Start Broad, Then Narrow**
   - First run: Broad topic (e.g., "AI tools")
   - Review results, identify sub-niches
   - Second run: Specific niche (e.g., "ChatGPT prompts for real estate")

3. **Compare Multiple Niches**
   - Run script for 3-5 related niches
   - Compare PDF potential scores
   - Choose highest-scoring niche with personal interest/expertise

4. **Integrate with PDF Creation Workflow**
   - Research → Select template → Create outline → Generate content → Design → Publish
   - This script handles the research phase (saves 2-3 hours)
   - Feeds directly into `generate_content.py` and `generate_pdf.py`

5. **Archive Reports**
   - Keep reports in `.tmp/` for 30 days
   - Move valuable research to `deliverables/` or project-specific folders
   - Reference past research when validating ongoing trends

### Dependencies:

- Python 3.8+
- Standard library only (no external packages required for basic functionality)
- Optional: `requests` library for Google Search API integration

### Common Mistakes to Avoid:

- ❌ Running script without Exploding Topics data (works, but less valuable)
- ❌ Ignoring the "PDF potential score" - it's calculated to identify best opportunities
- ❌ Not executing the recommended search queries (script provides the roadmap, you need to gather examples)
- ❌ Choosing topics based solely on growth without considering PDF format suitability
- ✅ Use this as **Step 1** in your PDF product pipeline, not a complete solution

### Integration with Other Scripts:

This script is designed to feed into your existing PDF pipeline:

```
research_pdf_products.py  (You are here - 5 min)
    ↓
generate_content.py  (Use recommended template structure - 30 min)
    ↓
generate_pdf.py  (Format into professional PDF - 15 min)
    ↓
upload_to_gumroad.py  (Publish - 10 min)
```

**Total Time: ~1 hour** (vs. 2-4 hours manual research + creation)

## Changelog

- **2025-11-29**: Initial creation
  - Core research automation engine
  - Exploding Topics CSV/JSON integration
  - PDF potential scoring algorithm
  - Markdown report generation
  - Parameterized CLI interface
  - Flexible column name matching for various CSV formats
