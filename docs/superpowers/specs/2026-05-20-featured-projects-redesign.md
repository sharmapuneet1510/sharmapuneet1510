# Featured Projects Redesign: Vertical Layout with Category Grouping

**Date:** 2026-05-20  
**Scope:** Reorganize Featured Projects section in README.md from horizontal table to vertical categorized layout  
**Status:** Design Approved

---

## Goal

Redesign the Featured Projects section to display projects vertically grouped by category (AI & Agentic Systems, Developer Tools) with full-width detailed cards, ordered by importance/prominence within each category.

---

## Current State

**Current Layout:** 5-column HTML table, all projects side-by-side
- awesome-prompts (AI/Agentic)
- doc-based-rag (AI)
- agentic-ai-lab (AI/Research)
- guardian (AI/ML/Safety)
- workstream (Developer Tools)

**Problem:** Horizontal layout doesn't scale well, unclear categorization, projects compete visually

---

## Proposed Design

### Category Structure

**Category 1: 🤖 AI & Agentic Systems** (4 projects)
Ordered by importance/prominence:
1. **awesome-prompts** — Full-Lifecycle Feature Builder (Production Ready, v4.2.0)
2. **agentic-ai-lab** — Research hub for autonomous AI pipelines (Active)
3. **doc-based-rag** — Transform documentation into interactive AI knowledge bases (Incubating)
4. **guardian** — Multi-camera real-time safety monitoring system (Building)

**Category 2: 🛠️ Developer Tools** (1 project)
1. **workstream** — Desktop release management and workflow platform (Active)

### Card Format

Each project displays as a markdown block with:
- **Heading:** `### [emoji] [Project Name]`
- **Description:** One-line value proposition
- **Stack:** Technologies/tools used
- **Additional Context:** Features, capabilities (if applicable)
- **Status:** Status badge (🟢 Production Ready / 🟡 Incubating / 🟢 Active / 🔵 Building)
- **Links:** [View Repo] and other relevant links

### Markdown Structure

```markdown
## 🚀 Featured Projects

### 🤖 AI & Agentic Systems

#### 🔄 awesome-prompts
End-to-end autonomous development: code generation → test validation → auto-documentation...
**Stack:** Python, LangChain, Claude, Multiple LLMs
**Status:** 🟢 Production Ready (v4.2.0)
[View Repo] | [Docs] | [Release]

#### 🧠 agentic-ai-lab
Research hub for autonomous AI pipelines and workflows
**Stack:** Python, LangChain, RAG
**Status:** 🟢 Active
[View Repo]

#### 📚 doc-based-rag
Transform documentation into interactive AI knowledge bases
**Stack:** FastAPI, Vector DB, Python
**Status:** 🟡 Incubating
[View Repo]

#### 👁️ guardian
Multi-camera real-time safety monitoring system
**Stack:** AI/ML, Computer Vision
**Status:** 🔵 Building
[View Repo]

### 🛠️ Developer Tools

#### 📋 workstream
Desktop release management and workflow platform
**Stack:** Electron, TypeScript
**Status:** 🟢 Active
[View Repo]
```

### Visual Characteristics

- **Layout:** Vertical (top to bottom), full-width
- **Organization:** Category groups with 4-level heading hierarchy
  - `## 🚀 Featured Projects` (main section)
  - `### 🤖 Category Name` (category headers)
  - `#### [emoji] Project Name` (project titles)
- **Spacing:** Natural markdown breaks between projects
- **Styling:** Consistent across all cards (no special HTML, pure markdown)
- **Scalability:** Easy to add/remove projects or categories

---

## Ordering Logic

**Within each category:** Ordered by importance/prominence
- awesome-prompts leads AI & Agentic Systems category (flagship product)
- Others ordered by: Production Ready → Active → Incubating → Building
- Within same status, ordered by relevance/maturity

---

## Implementation Details

### File to Update
`README.md` lines 58-130 (current Featured Projects section)

### Changes Required
1. Replace HTML table structure with markdown sections
2. Reorganize projects into two category groups
3. Reorder projects within AI & Agentic Systems (awesome-prompts first, then agentic-ai-lab, doc-based-rag, guardian)
4. Update heading levels to reflect category hierarchy
5. Maintain all project information (stack, status, links) in new format

### No Deletions
- No projects removed
- No information lost
- All links preserved

---

## Benefits

✅ **Readability:** Vertical layout matches natural reading flow  
✅ **Organization:** Clear category grouping helps navigation  
✅ **Scalability:** Easy to add/remove projects or categories later  
✅ **Maintainability:** Pure markdown, no HTML styling complexity  
✅ **GitHub-friendly:** Renders beautifully on GitHub with native markdown  
✅ **Visual Hierarchy:** Heading levels clearly show category structure  
✅ **Flagship Prominence:** awesome-prompts leads category without special styling  

---

## Success Criteria

✅ Projects displayed vertically (top to bottom)  
✅ Projects grouped into two categories (AI & Agentic Systems, Developer Tools)  
✅ awesome-prompts positioned first in AI category (flagship)  
✅ All project information preserved and readable  
✅ All links functional  
✅ Markdown formatting clean and consistent  
✅ GitHub rendering displays category structure clearly  
✅ No HTML tables or complex styling needed
