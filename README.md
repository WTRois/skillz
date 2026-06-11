# 🛠️ Full Project Analyzer Skill

A comprehensive, zero-dependency codebase analysis skill and instructions template designed for agentic AI architectures (such as Zed, Cursor, Claude Projects, and GitHub Copilot).

It guides LLMs to systematically auto-detect programming languages, frameworks, ORMs, and databases, map entry points, trace structural architectures, extract schemas, and generate beautiful, standardized Markdown documentation accompanied by renderable Mermaid diagrams.

---

## 🚀 How It Works (The Core Pipeline)

The instruction sets in this skill guide the AI through a structured multi-phase workflow:
1. **Phase 0 (Stack Auto-Detection)**: Inspects files against a robust signature matrix to compile a concrete `[STACK]` configuration.
2. **Phase 1 (Reconnaissance)**: Swiftly pinpoints main entry point files and scopes codebase size without wasting context window tokens.
3. **Phase 2 (Deep Analysis)**: Digs into target layers, reading database migrations, route maps, and config files relative to the detected tech stack.
4. **Phase 3 (Diagram Generation)**: Designs System Architecture Flowcharts, ER diagrams (for relational databases), and Sequence Diagrams while observing strict schema rules.
5. **Phase 4 (Markdown Output)**: Compiles the final document with zero-placeholder markdown reporting.

---

## ⚙️ Setup and Integration across Agents

### 1. Zed Editor (Agentic Mode)

Zed natively supports **Agent Skills**. To install this helper globally:

1. Create a directory named `full-project-analyzer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/full-project-analyzer
   ```
2. Copy the `full-project-analyzer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp full-project-analyzer.md ~/.agents/skills/full-project-analyzer/SKILL.md
   ```
3. Restart your Zed Editor or trigger the Assistant Panel. You can type `/` to see the skill registered, or simply prompt: 
   > *"Analyze this project and document it."*

---

### 2. Cursor Editor (`.cursorrules`)

Cursor utilizes `.cursorrules` inside the root of your project to govern AI interactions and answers.

1. Create a `.cursorrules` file in the root of your repository (or append to your existing one).
2. Paste the contents of `full-project-analyzer.md` as custom system instructions inside `.cursorrules`.
3. Highlight the file in Composer or chat using `@.cursorrules` and ask:
   > *"Run project analyzer rules to document this repository."*

---

### 3. GitHub Copilot (`.github/copilot-instructions.md`)

GitHub Copilot (in VS Code/GitHub) automatically reads workspace prompt suggestions from a designated markdown file.

1. Create the directories and file in your project:
   ```bash
   .github/copilot-instructions.md
   ```
2. Insert a clear preamble pointing to the instructions block, followed by the content of `full-project-analyzer.md`:
   ```markdown
   # Copilot Instructions

   When asked to document, analyze, or map the system architecture of this project, execute the rules described below:

   [Paste the content of full-project-analyzer.md here]
   ```
3. Issue a command in Copilot Chat:
   > *"@workspace generate architecture and database documentation."*

---

### 4. Claude Projects (Project Instructions)

If you use Anthropic’s Claude Web interface, you can leverage "Projects" to keep custom instructions saved.

1. Open your project on Claude.
2. Navigate to **Project Instructions** in the right-side panel.
3. Copy/paste the full content of `full-project-analyzer.md` into the instructions box and save.
4. Upload your codebase files (or a ZIP folder of the codebase) and prompt:
   > *"Analyze this workspace."*

---

## 🎯 Trigger Keywords

The agent will automatically latch onto this skill when you use keywords like:
- `"analyze this project"` / `"analisis repository ini"`
- `"document this codebase"` / `"buat dokumentasi kode"`
- `"explain how this repo works"` / `"bagaimana cara kerja project ini"`
- `"create system architecture diagram"` / `"buat diagram arsitektur"`
- `"what tables do we have in the database"` / `"buat ERD dari skema tabel"`

---

## 🛑 Critical Rules for Diagram Previews

* **No Inline HTML in Mermaid**: Many Markdown/preview engines (including Zed's built-in previewer) will crash or fail to output if your Mermaid charts contain raw HTML tags (e.g., `<br>`, `<b>`, `<i>`). **Keep diagrams strictly plain text.**
* **Consistency in Output Language**: The analyzer is instructed to draft the final markdown report in the **same language** that you used to query it (e.g. Indonesian if queried in Indonesian, or English if queried in English).
