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
- **Interactive Action Query**: Asks the user for confirmation before executing `git commit` and `git push` to their active branch.

### 3. 🎨 Component Generator (`component-generator.md`)
Detects the active UI framework (React, Vue, Svelte, Angular, Astro, etc.) and codebase styles (Tailwind, TypeScript, CSS modules) to generate robust, typed, accessibility-compliant components.
- **Interactive Action Query**: Analyzes existing project directories and asks the user for permission to write the generated component file to the recommended project path (e.g. `src/components/{ComponentName}.tsx`).

### 4. 🔎 Code Reviewer (`code-reviewer.md`)
Systematically reviews code across four dimensions — Bug, Security, Performance, and Convention — producing a structured report with severity ratings, exact locations, and concrete fix suggestions with corrected code samples.
- **Interactive Action Query**: After presenting the review report, asks the user whether they want the agent to automatically apply the suggested fixes to the affected files.

### 5. 🗄️ DB Schema Designer (`db-schema-designer.md`)
Designs comprehensive relational database schemas from business or technical requirement descriptions. Generates ERD diagrams (Mermaid), normalized migration SQL, a relation map with ON DELETE policies, and index recommendations.
- **Interactive Action Query**: After generating the schema, asks the user for permission to write the schema Markdown document and individual migration SQL files to the project's recommended paths.

### 6. 🔗 API Designer (`api-designer.md`)
Generates complete REST API contracts (method, path, request/response JSON schemas, HTTP status codes, error envelopes, auth requirements) before any implementation code is written. Contract-first design for frontend/backend alignment.
- **Interactive Action Query**: After generating the contract, asks the user for permission to save the API contract document to a recommended file path (e.g. `docs/api-contract-[domain].md`).

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

#### To setup `component-generator`:
1. Create a directory named `component-generator` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/component-generator
   ```
2. Copy the `component-generator.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp component-generator.md ~/.agents/skills/component-generator/SKILL.md
   ```

#### To setup `code-reviewer`:
1. Create a directory named `code-reviewer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/code-reviewer
   ```
2. Copy the `code-reviewer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp code-reviewer.md ~/.agents/skills/code-reviewer/SKILL.md
   ```

#### To setup `db-schema-designer`:
1. Create a directory named `db-schema-designer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/db-schema-designer
   ```
2. Copy the `db-schema-designer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp db-schema-designer.md ~/.agents/skills/db-schema-designer/SKILL.md
   ```

#### To setup `api-designer`:
1. Create a directory named `api-designer` under your user's global agent skills folder:
   ```bash
   mkdir -p ~/.agents/skills/api-designer
   ```
2. Copy the `api-designer.md` file into that folder and name it **`SKILL.md`**:
   ```bash
   cp api-designer.md ~/.agents/skills/api-designer/SKILL.md
   ```

*Restart your Zed Editor or trigger the Assistant Panel. You can type `/` to see the skills registered, or type standard trigger keywords.*

---

### 2. Cursor Editor (`.cursorrules`)

Cursor utilizes `.cursorrules` located in the root of your project to govern AI interactions.

1. Create a `.cursorrules` file in the root of your repository (or append to your existing one).
2. Append the contents of `full-project-analyzer.md`, `pr-writer.md`, `component-generator.md`, `code-reviewer.md`, `db-schema-designer.md`, and `api-designer.md` as custom system instructions inside `.cursorrules`.
3. Reference them in the Composer/Chat panel using `@.cursorrules` and ask:
   > *"Run component-generator rules to build a UserListItem component."*

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

   - When asked to write UI components, execute the rules described in:
     [Paste content of component-generator.md here]

   - When asked to review code quality, execute the rules described in:
     [Paste content of code-reviewer.md here]

   - When asked to design a database schema or ERD, execute the rules described in:
     [Paste content of db-schema-designer.md here]

   - When asked to design or plan a REST API contract, execute the rules described in:
     [Paste content of api-designer.md here]
   ```

---

### 4. Claude Projects (Project Instructions)

If you use Anthropic’s Claude Web interface, you can leverage "Projects" to keep custom instructions saved.

1. Open your project on Claude.
2. Navigate to **Project Instructions** in the right-side panel.
3. Copy/paste the full content of the desired skills into the instructions box and save.

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

### For `component-generator`:
- `"generate component"` / `"buatkan komponen"`
- `"create button/modal/form/table/card"` / `"bikin card UI"`
- `"component-generator"` / `"build component [component name]"`

### For `code-reviewer`:
- `"review this code"` / `"review kode ini"`
- `"code review"` / `"check for bugs"` / `"cek bug"`
- `"security audit"` / `"is this code safe?"`
- `"code-reviewer"` / `"review new feature"`

### For `db-schema-designer`:
- `"design database schema"` / `"buat schema database"`
- `"create ERD"` / `"design ERD for [app]"`
- `"generate migration SQL"` / `"buatkan tabel database"`
- `"table relationships"` / `"foreign key design"`
- `"database design for [domain]"` / `"db-schema-designer"`

### For `api-designer`:
- `"design API"` / `"create API contract"`
- `"what endpoints do I need"` / `"API spec"`
- `"build API for feature X"` / `"plan endpoints"`
- `"request/response schema"` / `"before I build the API"`
- `"api-designer"` / `"OpenAPI"` / `"swagger spec"`

---

## 🛑 Critical Guardrails

* **No Inline HTML in Mermaid**: Many Markdown/preview engines (including Zed's built-in previewer) will crash or fail to output if your Mermaid charts contain raw HTML tags (e.g., `<br>`, `<b>`, `<i>`). **Keep diagrams strictly plain text.**
* **Consistency in Output Language**: The analyzers are instructed to draft the output in the **same language** that you used to query them (e.g. Indonesian if queried in Indonesian, or English if queried in English).
