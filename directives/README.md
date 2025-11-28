# Directives Layer

This directory contains SOPs (Standard Operating Procedures) written in Markdown.

## Purpose

Directives are natural language instructions that define:
- **Goals**: What needs to be accomplished
- **Inputs**: What data or parameters are needed
- **Tools/Scripts**: Which execution scripts to use
- **Outputs**: What the result should be
- **Edge Cases**: Known issues and how to handle them

## Directive Format

Each directive should follow this structure:

```markdown
# [Directive Name]

## Goal
What this directive accomplishes

## Inputs
- Required data/parameters
- Where to get them

## Tools/Scripts
- Which scripts in `execution/` to use
- Order of operations

## Outputs
- What gets produced
- Where it goes (cloud service, file, etc.)

## Edge Cases
- Known issues
- API limits
- Timing considerations
- Error handling strategies

## Notes
- Best practices
- Performance considerations
- Recent learnings
```

## Living Documents

Directives are **living documents**. When you discover:
- API constraints
- Better approaches
- Common errors
- Timing expectations

Update the directive to capture this knowledge.

## Important

⚠️ **Do not create or overwrite directives without asking unless explicitly told to.**

Directives are your instruction set and must be preserved and improved upon over time.

## Examples

Create directives for workflows like:
- `scrape_website.md`
- `generate_report.md`
- `process_data.md`
- `send_email.md`
- etc.
