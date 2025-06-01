# PLANC-CLI

`Not the first, or second, but the only plan.`

**PLANC-CLI** is a powerful and intelligent command-line interface that automates the end-to-end process of resume and cover letter generation. It blends structured user memory, LLM-powered job description parsing, and LaTeX/Markdown generation into a seamless, session-aware workflow designed for power users and automation.

---

## `Features at a Glance`

* Interactive `planc setup` for API keys and initial config

* Session-aware CLI: upload a JD once, resume where you left off

* Google Gemini-powered job description parsing and metadata extraction

* Structured resume generation in LaTeX (with `.tex`, `.pdf`, clipboard, stdout support)

* AI-assisted, well-formatted cover letters in `.txt` and `.pdf`

* Full CRUD and deduplication support for user memory (name, email, skills, etc.)

* Modular prompt system with editable templates and update support

* Clean folder hierarchy by date and company/job-title parsed from JD

* Complete logging for every session (CSV + optional JSON export)

* One-command session replays, reusable job applications

* Bootstrap script (`init-env`) for quick setup of dependencies

* Future extensibility with prompt syncing and local inference support

* Smart, session-aware command flow

* One JD upload powers multiple downstream commands

* Google Gemini-powered job description parsing

* Resume generation with structured LaTeX output

* Tailored, professional cover letter generation (text + PDF)

* Persistent user profile with full CRUD and deduplication

* Daily-organized file storage with clean folder naming

* Application logging with session snapshots

* Clipboard support, Overleaf export, reusability

---

## `Tech Stack`

| Component        | Tool / Library      | Purpose                                       |
| ---------------- | ------------------- | --------------------------------------------- |
| CLI Framework    | Typer               | Command routing and argument parsing          |
| LLM Integration  | Google Gemini       | Job description parsing, cover letter writing |
| Data Modeling    | Pydantic            | Schema validation for resume, JD, and user    |
| File Handling    | Pathlib, shutil, os | Folder structure and file operations          |
| Clipboard Access | pyperclip           | Copy LaTeX or cover letter to clipboard       |
| PDF Generation   | weasyprint / pdfkit | Convert text/Markdown to styled PDF           |
| Logging          | CSV, JSON           | Track session metadata and output references  |


---

## `CLI Command Reference`

### Setup

| Command          | Description                                                                       |
| ---------------- | --------------------------------------------------------------------------------- |
| `planc setup`    | Interactive setup for API keys and configuration. Creates `~/.planc/config.json`. |
| `planc init-env` | Optional: bootstraps environment, checks dependencies, creates config folders.    |

### Job Description

| Command               | Description                                     |
| --------------------- | ----------------------------------------------- |
| `planc -jd """..."""` | Uploads new JD, parses metadata, starts session |
| `planc status`        | View current session status & file pointers     |
| `planc clear`         | Reset session and clear state                   |

### Resume Generation

| Command             | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `planc -r`          | Generate LaTeX + PDF resume (skip if already generated) |
| `planc -r --copy`   | Copy LaTeX code to clipboard for Overleaf               |
| `planc -r --stdout` | Output LaTeX to terminal directly                       |
| `planc --force`     | Regenerate resume forcibly, even if present             |

### Cover Letter

| Command             | Description                                   |
| ------------------- | --------------------------------------------- |
| `planc -c`          | Generate tailored cover letter (text + PDF)   |
| `planc -c --copy`   | Copy letter content to clipboard              |
| `planc -c --stdout` | Print letter to terminal for editing or reuse |

### User Memory (`fill`)

| Command                             | Description                                      |
| ----------------------------------- | ------------------------------------------------ |
| `planc fill init`                   | Setup wizard for user info (name, email, skills) |
| `planc fill show`                   | View saved memory snapshot                       |
| `planc fill reset`                  | Reset entire memory state                        |
| `planc fill add --field --value`    | Add item to list field (deduplicated)            |
| `planc fill update --field --value` | Update scalar field like name or email           |
| `planc fill remove --field --value` | Remove item from list field                      |
| `planc fill delete --field`         | Delete a full field from memory                  |

### Logs

| Command                              | Description                                     |
| ------------------------------------ | ----------------------------------------------- |
| `planc log`                          | View full application history (CSV)             |
| `planc log --last`                   | View most recent session entry                  |
| `planc log --filter date=YYYY-MM-DD` | Filter logs by date string                      |
| `planc log --export json`            | Export structured log as JSON for dashboard use |

### Utilities

| Command                    | Description                                          |
| -------------------------- | ---------------------------------------------------- |
| `planc export --zip`       | Export entire session as Overleaf-ready .zip archive |
| `planc debug session`      | Print raw session.json for diagnostics               |
| `planc debug paths`        | Output all key file paths for this session           |
| `planc reapply` (optional) | Reuse past session to apply to a new JD              |

---

## `Roadmap (6–7 Day Rollout)`
`NOTE: This is a summer project of mine and may not follow the below timeline exactly, Delays due to travel and "fun stuff" is unavoidable`

| Session | Focus Area             | Deliverables                                   |
| --- | ---------------------- | ---------------------------------------------- |
| 1   | Session & JD Handling  | Folder logic, JD parser, session engine        |
| 2   | Resume Generator       | `.tex` + `.pdf`, copy/stdout support           |
| 3   | Cover Letter Generator | `.txt` + `.pdf` writer from LLM/Markdown       |
| 4   | User Memory (`fill`)   | Full CRUD CLI with deduplication support       |
| 5   | Logging & Persistence  | CSV logs, metadata writebacks                  |
| 6   | Utilities & Debug      | `status`, `debug`, zip/export features         |
| 7   | Testing & Polish       | Refactors, UX refinements, README finalization |

---

## `License`

MIT

---

## `Author`

Swapnil Deb
