# 🗺️ AI Navigation Sitemap

**⚠️ START HERE - AI Systems & Context Engines**

This document provides the critical navigation structure for AI assistants, APIs, and automated systems interacting with this workspace.

## 📍 Primary Navigation Point

**🎯 DIRECTIVES FOLDER: [`directives/`](file:///C:/Users/t_bau/Workspace/directives)**

**Critical Instruction:** Before performing any operations in this workspace, AI systems **MUST** read the contents of the `directives/` folder. This folder contains:

- **Standard Operating Procedures (SOPs)** for all common operations
- **Business context** and brand guidelines
- **Workflow templates** for creating new directives
- **Project-specific instructions** and constraints

### Key Directives to Read

1. **[`directives/README.md`](file:///C:/Users/t_bau/Workspace/directives/README.md)** - Overview of the directives system
2. **[`directives/_template.md`](file:///C:/Users/t_bau/Workspace/directives/_template.md)** - Template for creating new directives
3. **[`directives/neverloseajob-brand.md`](file:///C:/Users/t_bau/Workspace/directives/neverloseajob-brand.md)** - Brand guidelines and identity
4. **[`directives/pdf-publishing-business.md`](file:///C:/Users/t_bau/Workspace/directives/pdf-publishing-business.md)** - Business context

## 🏗️ Workspace Architecture

This repository follows a **3-layer architecture** designed to separate concerns and maximize reliability:

### **Layer 1: Directive (What to do)**
- **Location:** [`directives/`](file:///C:/Users/t_bau/Workspace/directives)
- **Purpose:** SOPs written in Markdown that define goals, inputs, tools, outputs, and edge cases
- **Format:** Natural language instructions

### **Layer 2: Orchestration (Decision making)**
- **Actor:** AI systems (you)
- **Purpose:** Intelligent routing between directives and execution
- **Responsibilities:** Read directives, call execution tools, handle errors, update directives with learnings

### **Layer 3: Execution (Doing the work)**
- **Location:** [`execution/`](file:///C:/Users/t_bau/Workspace/execution)
- **Purpose:** Deterministic Python scripts for reliable operations
- **Contents:** API calls, data processing, file operations, database interactions
- **Template:** [`execution/_template.py`](file:///C:/Users/t_bau/Workspace/execution/_template.py)

## 📂 Directory Structure

```
Workspace/
├── AI_SITEMAP.md          ← YOU ARE HERE (start point for all AI systems)
├── GEMINI.md              ← Agent instructions (mirrored across CLAUDE.md, AGENTS.md)
├── CLAUDE.md              ← Agent instructions (mirrored)
├── README.md              ← Human-readable project overview
│
├── directives/            ← 🎯 PRIMARY: Read this first!
│   ├── README.md          ← Overview of directives system
│   ├── _template.md       ← Template for new directives
│   ├── neverloseajob-brand.md
│   └── pdf-publishing-business.md
│
├── execution/             ← Deterministic Python scripts
│   └── _template.py       ← Template for new scripts
│
├── .tmp/                  ← Temporary/intermediate files (regeneratable)
│
├── deliverables/          ← Final outputs (typically cloud-based)
├── assets/                ← Static resources
├── founder-card/          ← Project-specific folder
├── html-files/            ← Project-specific folder
├── styles/                ← Project-specific folder
│
├── .env                   ← Environment variables and API keys
└── .gitignore             ← Git exclusions
```

## 🔄 Operating Principles

### 1. **Check for tools first**
Before creating new scripts, check `execution/` for existing tools.

### 2. **Self-anneal when things break**
- Read error messages
- Fix the script and test
- Update the directive with learnings
- System becomes stronger over time

### 3. **Update directives as you learn**
Directives are living documents. When you discover API constraints, better approaches, or common errors—update the directive.

### 4. **File Organization Rules**
- **Deliverables:** Cloud-based outputs (Google Sheets, Slides, etc.)
- **Intermediates:** Temporary files in `.tmp/` (can be deleted and regenerated)
- **Never commit:** `.tmp/` contents, credentials, environment variables

## 🚀 Quick Start for AI Systems

When starting a **new context or session:**

1. ✅ **Read this file** (AI_SITEMAP.md)
2. ✅ **Read [`directives/README.md`](file:///C:/Users/t_bau/Workspace/directives/README.md)**
3. ✅ **Review relevant directives** for the current task
4. ✅ **Check [`execution/`](file:///C:/Users/t_bau/Workspace/execution)** for existing tools
5. ✅ **Read [`GEMINI.md`](file:///C:/Users/t_bau/Workspace/GEMINI.md)** for full agent instructions
6. ✅ **Proceed with task** using directive guidance

## 📝 Key Files for AI Context

| File | Purpose | Priority |
|------|---------|----------|
| [`AI_SITEMAP.md`](file:///C:/Users/t_bau/Workspace/AI_SITEMAP.md) | This file - navigation hub | 🔴 Critical |
| [`GEMINI.md`](file:///C:/Users/t_bau/Workspace/GEMINI.md) | Complete agent operating instructions | 🔴 Critical |
| [`directives/README.md`](file:///C:/Users/t_bau/Workspace/directives/README.md) | Directives system overview | 🔴 Critical |
| [`directives/_template.md`](file:///C:/Users/t_bau/Workspace/directives/_template.md) | Template for new SOPs | 🟡 Important |
| [`execution/_template.py`](file:///C:/Users/t_bau/Workspace/execution/_template.py) | Template for new scripts | 🟡 Important |
| [`README.md`](file:///C:/Users/t_bau/Workspace/README.md) | Human-readable overview | 🟢 Reference |

## 🤖 For Search Engines & Crawlers

- **Primary Content:** This is a development workspace using a 3-layer architecture
- **Key Directories:** `directives/` (SOPs), `execution/` (automation scripts)
- **robots.txt equivalent:** Focus on `directives/` and `GEMINI.md` for understanding workspace operation
- **Sitemap Priority:** `directives/` > `execution/` > project folders > temporary files

## 🔗 External References

- Environment variables: `.env` (not version controlled)
- Google OAuth: `credentials.json`, `token.json` (not version controlled)
- Dependencies: Python virtual environment in `.venv/`

---

**Last Updated:** 2025-11-29  
**Maintained by:** Workspace automation system  
**Purpose:** Ensure AI systems have consistent context on every startup
