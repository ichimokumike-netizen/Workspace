# 3-Layer Architecture Workspace

This workspace follows a 3-layer architecture that separates concerns to maximize reliability.

## Architecture Overview

### Layer 1: Directive (What to do)
- **Location**: `directives/`
- **Purpose**: SOPs written in Markdown
- **Content**: Goals, inputs, tools/scripts to use, outputs, and edge cases
- Natural language instructions, like you'd give a mid-level employee

### Layer 2: Orchestration (Decision making)
- **Role**: AI Agent (Gemini/Claude)
- **Purpose**: Intelligent routing and decision-making
- **Responsibilities**: 
  - Read directives
  - Call execution tools in the right order
  - Handle errors
  - Ask for clarification
  - Update directives with learnings

### Layer 3: Execution (Doing the work)
- **Location**: `execution/`
- **Purpose**: Deterministic Python scripts
- **Content**: API calls, data processing, file operations, database interactions
- **Key**: Reliable, testable, fast

## Directory Structure

```
.
├── .tmp/              # Intermediate files (never commit, always regenerated)
├── execution/         # Python scripts (deterministic tools)
├── directives/        # SOPs in Markdown (instruction set)
├── .env               # Environment variables and API keys
├── credentials.json   # Google OAuth credentials (in .gitignore)
├── token.json         # Google OAuth token (in .gitignore)
├── GEMINI.md          # Agent instructions
└── README.md          # This file
```

## Operating Principles

1. **Check for tools first**: Before writing a script, check `execution/` per your directive
2. **Self-anneal when things break**: Fix errors, update tools, test, and document learnings
3. **Update directives as you learn**: Directives are living documents

## Self-annealing Loop

When something breaks:
1. Fix it
2. Update the tool
3. Test tool, make sure it works
4. Update directive to include new flow
5. System is now stronger

## Getting Started

1. Add your API keys to `.env`
2. Create directives in `directives/` for your workflows
3. Write execution scripts in `execution/`
4. Let the AI orchestrate between the layers

## Key Principle

**Deliverables** go to cloud services (Google Sheets, Slides, etc.)  
**Intermediates** go to `.tmp/` and can be regenerated

---

*Be pragmatic. Be reliable. Self-anneal.*
