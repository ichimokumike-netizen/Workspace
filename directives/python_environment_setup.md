# Python Environment Setup

## Goal

Ensure all Python scripts in the `execution/` layer run within an isolated virtual environment (`.venv`) to maintain dependency isolation, reproducibility, and prevent conflicts between projects.

## What is `.venv`?

`.venv` is a **Python virtual environment directory** that:
- Creates an isolated Python environment for this project
- Contains its own Python interpreter and package installations
- Keeps project dependencies separate from system-wide Python packages
- Prevents dependency conflicts across different projects
- Enables reproducible environments across machines

## Directory Structure

```
.venv/
├── Scripts/           # Python executable and activation scripts (Windows)
├── Lib/              # Installed packages
└── pyvenv.cfg        # Configuration file
```

**Important:** `.venv` is already in `.gitignore` and should NEVER be committed to version control.

## Workflow

### 1. Activating the Virtual Environment

**Before running ANY Python script**, activate `.venv`:

```powershell
# Windows
.venv\Scripts\activate

# You'll see (.venv) appear in your prompt
```

### 2. Installing Dependencies

```powershell
# Install all dependencies from requirements.txt
pip install -r execution/requirements.txt

# Install individual packages (if needed)
pip install package-name

# Important: Update requirements.txt when adding new packages
pip freeze > execution/requirements.txt
```

### 3. Running Scripts

```powershell
# Always activate first
.venv\Scripts\activate

# Then run your script
python execution/my_script.py
```

### 4. Deactivating

```powershell
deactivate
```

## Script Creation & Placement

**The virtual environment does NOT affect where you create or organize scripts.**

- ✅ **Scripts still go in `execution/` folder** (no changes)
- ✅ **Use `execution/_template.py`** as your starting point
- ✅ **Follow the same file organization** as always
- ❌ **Never put scripts inside `.venv` folder**

## Dependencies Management

### Current Dependencies

All project dependencies are defined in `execution/requirements.txt`:

```
python-dotenv==1.0.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
gspread==5.12.0
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
qrcode[pil]
```

### Adding New Dependencies

When creating a new script that requires packages:

1. Activate `.venv`
2. Install the package: `pip install package-name`
3. Update requirements: `pip freeze > execution/requirements.txt`
4. Document the dependency in your script's docstring

### Importing Between Scripts

Scripts can still import from each other:

```python
# Example: Import from another execution script
from execution.get_current_datetime import get_eastern_time
```

## Edge Cases & Common Issues

### Issue: "Module not found" errors

**Cause:** Virtual environment not activated, or package not installed

**Solution:**
1. Activate `.venv`
2. Install missing package: `pip install package-name`
3. Update `requirements.txt`

### Issue: Different Python version

**Cause:** `.venv` was created with a different Python version

**Solution:**
```powershell
# Delete old .venv
Remove-Item -Recurse -Force .venv

# Create new one with current Python
python -m venv .venv

# Activate and reinstall dependencies
.venv\Scripts\activate
pip install -r execution/requirements.txt
```

### Issue: Script works locally but fails for other agents

**Cause:** Dependency not documented in `requirements.txt`

**Solution:** Always update `requirements.txt` after installing new packages

## Best Practices

1. **Always activate before running** - Make it muscle memory: activate, then run
2. **Keep requirements.txt updated** - Document every dependency
3. **Don't commit `.venv`** - It's in `.gitignore` for a reason (already configured)
4. **Pin versions** - Use `==` to specify exact versions (prevents breaking changes)
5. **Fresh install test** - Occasionally delete `.venv` and reinstall from `requirements.txt` to ensure it's complete

## Integration with 3-Layer Architecture

The virtual environment fits seamlessly into the 3-layer architecture:

**Layer 1 (Directives)** → Natural language SOPs (this file)
**Layer 2 (Orchestration)** → Agents read directives, activate `.venv`, call scripts
**Layer 3 (Execution)** → Scripts run in isolated environment with proper dependencies

## Quick Reference

```powershell
# Typical workflow
.venv\Scripts\activate              # Step 1: Activate
pip install -r execution/requirements.txt   # Step 2: Ensure deps
python execution/my_script.py       # Step 3: Run script
deactivate                          # Step 4: Deactivate when done
```

## Notes

- **Created:** 2025-12-05
- **Last Updated:** 2025-12-05
- **Owner:** System setup (applies to all agents)
- **Frequency:** Every time before running Python scripts
- **Priority:** Critical - failure to activate `.venv` can cause import errors or use wrong package versions
