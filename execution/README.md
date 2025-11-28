# Execution Layer

This directory contains deterministic Python scripts that handle the actual work.

## Purpose

- Handle API calls
- Process data
- Perform file operations
- Manage database interactions
- Other reliable, testable operations

## Guidelines

1. **Reliability**: Scripts should be deterministic and consistent
2. **Testing**: All scripts should be testable
3. **Documentation**: Comment your code well
4. **Environment**: Use `.env` for API keys and configuration
5. **Error Handling**: Handle errors gracefully and provide meaningful messages

## Creating New Scripts

Before creating a new script:
1. Check if a similar script already exists
2. Review the directive to understand requirements
3. Plan your inputs and outputs
4. Write clean, well-commented code
5. Test thoroughly
6. Update the relevant directive with usage instructions

## Example Script Structure

```python
"""
Script: example_script.py
Purpose: Brief description of what this script does
Inputs: What data/parameters it expects
Outputs: What it produces
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main function"""
    # Your code here
    pass

if __name__ == "__main__":
    main()
```

## Dependencies

Install Python dependencies as needed:
```bash
pip install python-dotenv
# Add other dependencies as required
```
