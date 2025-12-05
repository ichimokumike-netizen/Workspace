# Time Validation Protocol - Master Directive

**Created:** 2025-11-30
**Status:** Production Directive
**Priority:** CRITICAL - Mandatory for ALL agents in workspace
**Scope:** All AI agents (Claude, Olive, custom agents)

---

## Core Principle: VALIDATE TIME BEFORE EVERY EXECUTION

**RULE #1:** Every agent MUST validate current date/time before ANY execution
**RULE #2:** Time comes from authoritative NTP servers, NEVER from system clock alone
**RULE #3:** All agents share the same time source (`.tmp/current_time.json`)
**RULE #4:** Data freshness validation is MANDATORY for all research tasks
**RULE #5:** Time validation failures HALT execution immediately

---

## Why This Matters

### The Problem:
- System clocks can be wrong (misconfigured, timezone issues, not synced)
- LLM training data has cutoff dates - we need REAL current time
- Research requires strict data freshness (30 days for directories, 90 days for PDFs)
- Multiple agents need consistent time reference for data sharing

### The Solution:
- Query authoritative NTP servers (time.nist.gov, time.google.com, pool.ntp.org)
- Store verified time in workspace file accessible to all agents
- Validate all research data against this authoritative time
- Reject data that exceeds age limits

---

## The 2-Script Time Validation System

### Script 1: `execution/get_current_datetime.py`

**Purpose:** Get authoritative current time from NTP servers

**When to Run:**
- At the START of every agent execution session
- Before any research or data gathering
- When time data is stale (> 5 minutes old)
- After system clock changes or timezone updates

**How to Run:**
```bash
python execution/get_current_datetime.py
```

**What It Does:**
1. Queries NTP servers in priority order:
   - time.nist.gov (NIST - Most authoritative for US)
   - time.google.com (Google - Fast and reliable)
   - pool.ntp.org (NTP Pool - Fallback)
2. Converts UTC to Eastern Time (America/New_York)
3. Saves comprehensive time data to `.tmp/current_time.json`
4. Falls back to system time if all NTP servers fail (with warning)

**Output Structure** (`.tmp/current_time.json`):
```json
{
  "utc_time": "2025-11-30T17:18:01+00:00",
  "eastern_time": "2025-11-30T12:18:01-05:00",
  "timestamp": 1764523081.0,
  "iso_format": "2025-11-30T12:18:01-05:00",
  "date_only": "2025-11-30",
  "time_only": "12:18:01",
  "year": 2025,
  "month": 11,
  "day": 30,
  "hour": 12,
  "minute": 18,
  "second": 1,
  "weekday": "Sunday",
  "ntp_server": "time.nist.gov",
  "last_updated": "2025-11-30T17:18:02+00:00",
  "timezone": "America/New_York",
  "timezone_offset": "-0500",
  "is_dst": false
}
```

### Script 2: `execution/validate_search_dates.py`

**Purpose:** Validate that research data is within acceptable age limits

**When to Run:**
- Before using ANY external data source
- When validating research results
- Before writing content with statistics/case studies
- During quality assurance checks

**How to Use in Python:**
```python
from execution.validate_search_dates import validate_data_freshness

# Validate a single date
result = validate_data_freshness(
    data_date="2025-11-29",
    max_age_days=30,
    context="Market research from Gumroad"
)

if result['is_valid']:
    print(f"[OK] Data is fresh: {result['message']}")
    # Use the data
else:
    print(f"[ERROR] Data too old: {result['message']}")
    # Reject the data, get fresh data
```

**Batch Validation:**
```python
from execution.validate_search_dates import validate_multiple_dates

dates_to_check = [
    {"date": "2025-11-29", "context": "Source 1: Reddit post"},
    {"date": "2025-11-20", "context": "Source 2: Case study"},
    {"date": "2025-11-15", "context": "Source 3: Tool pricing"},
]

result = validate_multiple_dates(dates_to_check, max_age_days=30)

if result['all_valid']:
    print("[OK] All sources are fresh")
else:
    print(f"[ERROR] {result['invalid_count']} sources too old")
    # Show which ones failed
    for r in result['results']:
        if not r['is_valid']:
            print(f"  - {r['context']}: {r['age_days']:.1f} days old")
```

---

## Mandatory Time Validation Workflow

### Phase 1: Agent Initialization (ALWAYS FIRST)

**Every agent execution MUST start with:**

```python
import subprocess
import sys
import json
import os
from datetime import datetime

def initialize_agent():
    """
    Initialize agent with validated current time
    MUST be called before any other agent operations
    """
    print("[INIT] Initializing agent with NTP time validation...")

    # Step 1: Get current time from NTP
    result = subprocess.run(
        [sys.executable, "execution/get_current_datetime.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] Failed to get current time: {result.stderr}")
        raise Exception("Time validation failed - cannot proceed")

    # Step 2: Load validated time
    if not os.path.exists('.tmp/current_time.json'):
        raise Exception("Time file not created - cannot proceed")

    with open('.tmp/current_time.json', 'r') as f:
        time_data = json.load(f)

    # Step 3: Set agent time reference
    current_date = datetime.fromisoformat(time_data['eastern_time'])

    print(f"[OK] Agent time validated: {time_data['date_only']} {time_data['time_only']} Eastern")
    print(f"[OK] NTP Server: {time_data['ntp_server']}")

    return time_data, current_date

# CALL THIS IMMEDIATELY
time_data, current_date = initialize_agent()
```

### Phase 2: Data Collection (VALIDATE EVERY SOURCE)

**When gathering research data:**

```python
from execution.validate_search_dates import validate_data_freshness

def collect_research_data(source_url, source_date, max_age_days=30):
    """
    Collect research data with mandatory freshness validation
    """
    # Validate source date BEFORE using the data
    validation = validate_data_freshness(
        data_date=source_date,
        max_age_days=max_age_days,
        context=f"Source: {source_url}"
    )

    if not validation['is_valid']:
        print(validation['message'])
        return None  # REJECT old data

    # Data is fresh - proceed with collection
    print(validation['message'])
    # ... collect and return data
```

### Phase 3: Pre-Execution Validation (BEFORE WRITING/PUBLISHING)

**Before generating any output:**

```python
def pre_execution_validation(collected_sources, max_age_days=30):
    """
    Validate all collected sources before proceeding
    """
    from execution.validate_search_dates import validate_multiple_dates

    # Format sources for batch validation
    dates_to_validate = [
        {"date": source['date'], "context": source['name']}
        for source in collected_sources
    ]

    # Batch validate
    result = validate_multiple_dates(dates_to_validate, max_age_days)

    if not result['all_valid']:
        print(f"\n[ERROR] Data freshness check FAILED")
        print(result['message'])
        print("\nInvalid sources:")
        for r in result['results']:
            if not r['is_valid']:
                print(f"  - {r['context']}: {r['age_days']:.1f} days old (limit: {max_age_days})")

        raise Exception("Cannot proceed with stale data")

    print(f"[OK] All {result['valid_count']} sources validated")
    return True
```

---

## Data Freshness Requirements by Product Type

### Directory/Filter Gap Strategy
- **Maximum data age:** 90 days
- **Rationale:** Strategic validation requires longer-term trend analysis to identify sustainable opportunities
- **Applies to:**
  - Reddit posts and comments (prefer < 30 days for trends)
  - Facebook group posts (prefer < 30 days for trends)
  - Google Business Profile reviews (< 90 days)
  - Tool pricing and features (verify within 7 days)
  - Search volume data (< 90 days, prefer current quarter)
  - Competitor listings (must be active today)

### PDF Information Products
- **Maximum data age:** 90 days (unless otherwise specified)
- **Rationale:** Strategic insights have longer shelf life than tactical tools
- **Applies to:**
  - Market research reports
  - Industry statistics
  - Case studies
  - Expert opinions
  - Tool comparisons

**EXCEPTION:** Breaking news, current events, or time-sensitive topics require 30-day limit

### General Research
- **Default maximum age:** 90 days
- **Always verify with directive:** Each product type may have specific requirements
- **When in doubt:** Use 90-day limit unless directive specifies otherwise

---

## Error Handling and Fallbacks

### Scenario 1: All NTP Servers Fail

**What happens:**
- `get_current_datetime.py` falls back to system clock
- Prints warning message
- Sets `ntp_server: "system_clock_fallback"` in output

**Agent response:**
```python
if time_data['ntp_server'] == 'system_clock_fallback':
    print("[WARN] Using system clock - NTP servers unavailable")
    print("[WARN] Verify system time is correct before proceeding")

    # Optionally: Require user confirmation
    user_confirm = input("System time may be inaccurate. Continue? (yes/no): ")
    if user_confirm.lower() != 'yes':
        raise Exception("User aborted due to time uncertainty")
```

### Scenario 2: Time File Missing

**What happens:**
- Agent tries to load `.tmp/current_time.json`
- File doesn't exist

**Agent response:**
```python
if not os.path.exists('.tmp/current_time.json'):
    print("[ERROR] Time validation file missing")
    print("[ACTION] Running time validation now...")

    # Auto-run get_current_datetime.py
    subprocess.run([sys.executable, "execution/get_current_datetime.py"])

    # Verify it worked
    if not os.path.exists('.tmp/current_time.json'):
        raise Exception("Failed to create time validation file")
```

### Scenario 3: Time File Stale

**What happens:**
- Time file is older than 5 minutes

**Agent response:**
```python
def is_time_file_stale(max_age_minutes=5):
    """Check if time file needs refresh"""
    if not os.path.exists('.tmp/current_time.json'):
        return True

    with open('.tmp/current_time.json', 'r') as f:
        time_data = json.load(f)

    last_updated = datetime.fromisoformat(time_data['last_updated'])
    age_minutes = (datetime.now() - last_updated).total_seconds() / 60

    return age_minutes > max_age_minutes

if is_time_file_stale():
    print("[INFO] Time file stale - refreshing from NTP...")
    subprocess.run([sys.executable, "execution/get_current_datetime.py"])
```

---

## Multi-Agent Time Sharing

### Shared Time Source
- **All agents** (Claude, Olive, custom agents) read from `.tmp/current_time.json`
- **Single source of truth** prevents time conflicts
- **Automatic synchronization** across agent communications

### Example: Agent A → Agent B Handoff

**Agent A (Research Agent):**
```python
# Agent A collects data
time_data, current_date = initialize_agent()

research_data = {
    "topic": "Commercial Kitchen Rentals",
    "sources": [...],
    "collected_at": time_data['eastern_time'],
    "collection_date": time_data['date_only']
}

# Save for Agent B
with open('.tmp/research_handoff.json', 'w') as f:
    json.dump(research_data, f)
```

**Agent B (Content Agent):**
```python
# Agent B loads research
time_data, current_date = initialize_agent()

with open('.tmp/research_handoff.json', 'r') as f:
    research_data = json.load(f)

# Validate research is still fresh
validation = validate_data_freshness(
    research_data['collected_at'],
    max_age_days=1,  # Research from Agent A should be < 1 day old
    context="Research from Agent A"
)

if not validation['is_valid']:
    print("[ERROR] Received stale research from Agent A")
    # Request fresh research
```

---

## Integration with Existing Directives

### How to Add Time Validation to Any Directive

**Step 1: Add to "Prerequisites" Section**

```markdown
## Prerequisites

**MANDATORY - Time Validation:**
Before executing this directive, MUST run:
```bash
python execution/get_current_datetime.py
```

This validates current date/time against NTP servers and stores result in `.tmp/current_time.json`.
All date comparisons and data freshness validations depend on this authoritative time source.
```

**Step 2: Add to "Execution" Section**

```markdown
## Execution

### Phase 0: Time Validation (ALWAYS FIRST)
1. Run `python execution/get_current_datetime.py`
2. Load time data from `.tmp/current_time.json`
3. Verify NTP validation succeeded
4. Set current_date for all subsequent operations

### Phase 1: [Your existing first phase]
...
```

**Step 3: Add Data Freshness Validation**

```markdown
## Data Freshness Requirements

**Maximum Data Age:** [30/90] days

**Validation Protocol:**
- All sources MUST be validated with `validate_search_dates.py`
- Sources exceeding age limit are REJECTED
- Agent must find fresh alternatives

**Example:**
```python
from execution.validate_search_dates import validate_data_freshness

result = validate_data_freshness(
    data_date=source_date,
    max_age_days=30,
    context=source_name
)

if not result['is_valid']:
    # REJECT - find fresh alternative
```
```

---

## Quality Assurance Checklist

**Before ANY agent execution:**

- [ ] `get_current_datetime.py` has been run
- [ ] `.tmp/current_time.json` exists and is valid
- [ ] NTP server validation succeeded (or fallback acknowledged)
- [ ] Current date loaded into agent memory
- [ ] Data age limits defined for this task

**During data collection:**

- [ ] Every source has a publication/access date
- [ ] Every date is validated with `validate_search_dates.py`
- [ ] Invalid sources are rejected (not just flagged)
- [ ] Fresh alternatives are found for rejected sources

**Before output generation:**

- [ ] All collected sources pass batch validation
- [ ] No sources exceed maximum age limit
- [ ] Time validation results are documented
- [ ] Output includes "Data current as of [date]" statement

---

## Common Patterns and Examples

### Pattern 1: Simple Agent Initialization

```python
#!/usr/bin/env python3
import subprocess
import sys
import json

# ALWAYS FIRST
subprocess.run([sys.executable, "execution/get_current_datetime.py"])

with open('.tmp/current_time.json', 'r') as f:
    time_data = json.load(f)

print(f"Agent running on: {time_data['date_only']}")

# ... rest of agent logic
```

### Pattern 2: Research Script with Validation

```python
from execution.validate_search_dates import validate_data_freshness

sources = [
    {"url": "reddit.com/r/...", "date": "2025-11-29", "content": "..."},
    {"url": "facebook.com/...", "date": "2025-11-20", "content": "..."},
]

valid_sources = []
for source in sources:
    result = validate_data_freshness(source['date'], max_age_days=30)
    if result['is_valid']:
        valid_sources.append(source)
    else:
        print(f"[SKIP] {source['url']}: {result['message']}")

print(f"[OK] Using {len(valid_sources)} of {len(sources)} sources")
```

### Pattern 3: Pre-Flight Check

```python
def pre_flight_check():
    """Run before any major operation"""
    checks = []

    # Check 1: Time file exists
    import os
    checks.append({
        "check": "Time file exists",
        "passed": os.path.exists('.tmp/current_time.json')
    })

    # Check 2: Time file is fresh (< 5 minutes)
    if checks[-1]['passed']:
        import json
        from datetime import datetime

        with open('.tmp/current_time.json', 'r') as f:
            time_data = json.load(f)

        last_updated = datetime.fromisoformat(time_data['last_updated'])
        age_seconds = (datetime.now() - last_updated).total_seconds()

        checks.append({
            "check": "Time file is fresh",
            "passed": age_seconds < 300  # 5 minutes
        })

    # Check 3: NTP validation succeeded
    if checks[0]['passed']:
        checks.append({
            "check": "NTP validation succeeded",
            "passed": time_data['ntp_server'] != 'system_clock_fallback'
        })

    # Report
    all_passed = all(c['passed'] for c in checks)
    for check in checks:
        status = "[OK]" if check['passed'] else "[FAIL]"
        print(f"{status} {check['check']}")

    return all_passed
```

---

## Troubleshooting

### Issue: "Time file not found"
**Solution:** Run `python execution/get_current_datetime.py`

### Issue: "All NTP servers failed"
**Causes:**
- No internet connection
- Firewall blocking NTP (port 123)
- NTP servers temporarily unavailable

**Solution:**
- Check internet connection
- Verify firewall settings (allow UDP port 123)
- Script will fall back to system clock (verify accuracy)

### Issue: "Data validation says everything is too old"
**Causes:**
- System clock is wrong
- Time file is stale
- Actually using old data

**Solution:**
1. Verify system clock: `python -c "import datetime; print(datetime.datetime.now())"`
2. Refresh time file: `python execution/get_current_datetime.py`
3. Check source dates are actually recent

### Issue: "Agent not using validated time"
**Causes:**
- Agent using `datetime.now()` instead of time file
- Agent not calling initialization

**Solution:**
- Update agent to load from `.tmp/current_time.json`
- Add mandatory `initialize_agent()` call

---

## Self-Annealing Protocol

### Learning from Time Validation Failures

**When time validation fails:**
1. Document the failure in `assets/agent_learnings/time_validation_failures.md`
2. Identify root cause (NTP failure, stale data, wrong dates, etc.)
3. Update relevant directive with prevention strategy
4. Test fix to ensure it works

**Example Learning Entry:**
```markdown
## 2025-11-30: All sources failed validation in Directory Agent

**Issue:** Directory agent collected Reddit posts but all failed freshness check

**Root Cause:** Agent was using post IDs instead of post dates for validation

**Fix:** Updated `reddit_mining.py` to extract actual post timestamp

**Prevention:** Added explicit date extraction requirements to directive

**Test:** Re-ran with fix - all validations passed
```

---

## Summary: The Time Validation Commandments

1. **THOU SHALT VALIDATE time from NTP before every execution**
2. **THOU SHALT NOT use system time without NTP validation**
3. **THOU SHALT REJECT data older than defined limits**
4. **THOU SHALT SHARE time source across all agents**
5. **THOU SHALT DOCUMENT all date sources with timestamps**
6. **THOU SHALT REFRESH time data when stale (> 5 minutes)**
7. **THOU SHALT HANDLE NTP failures gracefully**
8. **THOU SHALT VALIDATE before collecting, during collection, and before output**
9. **THOU SHALT UPDATE directives when learning from failures**
10. **THOU SHALT NEVER proceed with execution if time cannot be validated**

---

## File Locations

**Scripts:**
- `execution/get_current_datetime.py` - NTP time validation
- `execution/validate_search_dates.py` - Data freshness validation

**Data:**
- `.tmp/current_time.json` - Shared time source (all agents)

**Directives:**
- `directives/time_validation_protocol.md` - This file (master reference)
- All other directives should reference this protocol

---

**This directive is mandatory for ALL agents in the workspace.**

**Last Updated:** 2025-11-30
**Next Review:** 2025-12-30
