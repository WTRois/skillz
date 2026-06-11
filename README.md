# 🛠️ Global Developer Agent Skills

A collection of comprehensive, zero-dependency codebase helper skills and instruction templates designed for agentic AI architectures (such as Zed, Cursor, Claude Projects, and GitHub Copilot).

---

## 📂 Available Skills

### 1. 🔍 Full Project Analyzer (`full-project-analyzer.md`)
Guides LLMs to auto-detect programming languages, frameworks, ORMs, and databases, map entry points, trace modular architectures, extract schemas, and generate beautiful, standardized Markdown documentation accompanied by renderable Mermaid diagrams.
- **Automatic Output File**: Generates `project-full-summary-by-skillz.md` in the project's root folder.

### 2. 📝 PR Writer (`pr-writer.md`)
Analyzes git diff structures (staged, unstaged, or branch comparisons) to generate concise Conventional Commit messages and structured, copy-pasteable Pull Request (PR) descriptions.
- **Critical Zed Rule**: Automatically forces the `--no-pager` flag on Git CLI queries to prevent Zed's terminal shell from hanging.

---

## ⚙️ Setup and Integration across Agents

### 1. Zed Editor (Agentic Mode)

Zed natively supports **Agent Skills**. To install these helpers globally:

#### To setup `full-project-analyzer`:
1. Create a directory named `full-project-analyzer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/full-project-analyzer
   ```
2. Copy the `full-project-analyzer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp full-project-analyzer.md ~/.agents/skills/full-project-analyzer/SKILL.md
   ```

#### To setup `pr-writer`:
1. Create a directory named `pr-writer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/pr-writer
   ```
2. Copy the `pr-writer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp pr-writer.md ~/.agents/skills/pr-writer/SKILL.md
   ```

*Restart your Zed Editor or trigger the Assistant Panel. You can type `/` to see the skills registered, or type standard trigger keywords.*

---

### 2. Cursor Editor (`.cursorrules`)

Cursor utilizes `.cursorrules` located in the root of your project to govern AI interactions.

1. Create a `.cursorrules` file in the root of your repository (or append to your existing one).
2. Append the contents of `full-project-analyzer.md` and `pr-writer.md` as custom system instructions inside `.cursorrules`.
3. Reference them in the Composer/Chat panel using `@.cursorrules` and ask:
   > *"Run project analyzer rules to document this repository."*
   > OR
   > *"Write a PR description based on the pr-writer rules."*

---

### 3. GitHub Copilot (`.github/copilot-instructions.md`)

GitHub Copilot (in VS Code/GitHub) automatically reads workspace prompt suggestions from a designated markdown file.

1. Create the directories and file in your project:
   ```bash
   .github/copilot-instructions.md
   ```
2. Insert a clear preamble pointing to the instruction blocks, followed by the content of your desired skills:
   ```markdown
   # Copilot Instructions

   - When asked to document, analyze, or map the system architecture of this project, execute the rules described in:
     [Paste content of full-project-analyzer.md here]

   - When asked to write commits or pull requests, execute the rules described in:
     [Paste content of pr-writer.md here]
   ```
3. Issue a command in Copilot Chat:
   > *"@workspace generate draft documentation"* or *"@workspace write a PR from staged changes"*

---

### 4. Claude Projects (Project Instructions)

If you use Anthropic’s Claude Web interface, you can leverage "Projects" to keep custom instructions saved.

1. Open your project on Claude.
2. Navigate to **Project Instructions** in the right-side panel.
3. Copy/paste the full content of `full-project-analyzer.md` and/or `pr-writer.md` into the instructions box and save.

---

## 🎯 Trigger Keywords

### For `full-project-analyzer`:
- `"analyze this project"` / `"analisis repository ini"`
- `"document this codebase"` / `"buat dokumentasi kode"`
- `"explain how this repo works"` / `"bagaimana cara kerja project ini"`
- `"create system architecture diagram"` / `"buat diagram arsitektur"`
- `"what tables do we have in the database"` / `"buat ERD dari skema tabel"`

### For `pr-writer`:
- `"write a PR description"` / `"buat deskripsi PR"`
- `"generate a commit message"` / `"bikin commit message"`
- `"create a PR from diff"` / `"generate PR dari diff ini"`
- `"pr-writer"` / `"describe changes"`

---

## 🛑 Critical Guardrails

* **No Inline HTML in Mermaid**: Many Markdown/preview engines (including Zed's built-in previewer) will crash or fail to output if your Mermaid charts contain raw HTML tags (e.g., `<br>`, `<b>`, `<i>`). **Keep diagrams strictly plain text.**
* **Consistency in Output Language**: The analyzers are instructed to draft the output in the **same language** that you used to query them (e.g. Indonesian if queried in Indonesian, or English if queried in English).
