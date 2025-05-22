# PLANC-CLI

PLANC-CLI is a powerful command-line tool designed to automate and optimize the resume and cover letter creation process. It leverages LLMs to parse job descriptions, manages session state to streamline usage, and ensures all application artifacts are organized, logged, and reproducible.

---

## Features

* Session-aware command execution
* Upload a job description once and reuse across commands
* LLM-powered parsing of job descriptions
* Resume generation in LaTeX format
* Tailored cover letter generation (text + PDF)
* Full CRUD support for user profile memory
* Full deduplication support for all user fields
* Organized file storage by date and company/role
* Complete CSV logging of each application session
* Support for copy-to-clipboard and Overleaf exports

---

## Tech Stack

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

## Folder Structure

All application artifacts are saved under:

```
~/.planc/logs/YYYY-MM-DD/{company_title}/
```

Each session folder contains:

* resume\_{timestamp}.tex
* resume\_{timestamp}.pdf
* coverletter\_{timestamp}.txt
* coverletter\_{timestamp}.pdf
* job\_description.txt
* user\_snapshot.json
* meta.json (optional)

---

## CLI Commands

### Job Description

| Command               | Description                                       |
| --------------------- | ------------------------------------------------- |
| `planc -jd """..."""` | Upload new JD, parse company/title, start session |
| `planc status`        | View current session details                      |
| `planc clear`         | Reset current session                             |

### Resume Generation

| Command             | Description                                    |
| ------------------- | ---------------------------------------------- |
| `planc -r`          | Generate LaTeX + PDF resume (once per session) |
| `planc -r --copy`   | Copy LaTeX source to clipboard                 |
| `planc -r --stdout` | Print LaTeX to terminal                        |
| `planc --force`     | Regenerate resume if already generated         |

### Cover Letter

| Command             | Description                            |
| ------------------- | -------------------------------------- |
| `planc -c`          | Generate text + PDF cover letter       |
| `planc -c --copy`   | Copy cover letter text to clipboard    |
| `planc -c --stdout` | Print cover letter content to terminal |

### User Memory (`fill`)

| Command                             | Description                           |
| ----------------------------------- | ------------------------------------- |
| `planc fill init`                   | Setup wizard for name, skills, etc.   |
| `planc fill show`                   | Display saved profile                 |
| `planc fill reset`                  | Reset full user profile               |
| `planc fill add --field --value`    | Add item to list field (deduplicated) |
| `planc fill update --field --value` | Update scalar field                   |
| `planc fill remove --field --value` | Remove item from list field           |
| `planc fill delete --field`         | Delete entire field                   |

### Logs

| Command                              | Description                    |
| ------------------------------------ | ------------------------------ |
| `planc log`                          | Show application history (CSV) |
| `planc log --last`                   | Show most recent entry         |
| `planc log --filter date=YYYY-MM-DD` | Filter logs by date            |
| `planc log --export json`            | Export logs as JSON            |

### Utilities

| Command                    | Description                               |
| -------------------------- | ----------------------------------------- |
| `planc export --zip`       | Export resume/cover as Overleaf-ready zip |
| `planc debug session`      | Print raw session.json                    |
| `planc debug paths`        | Show current output paths                 |
| `planc reapply` (optional) | Reuse past session for a new application  |

---

## Roadmap (6-7 Days) 
`NOTE: This is a summer project of mine and may not follow the below timeline exactly, Delays due to travel and "fun stuff" is unavoidable`

| Day | Focus Area             | Goals                                            |
| --- | ---------------------- | ------------------------------------------------ |
| 1   | Session & JD Upload    | Folder structure, JD parsing, session.json       |
| 2   | Resume Generator       | Generate `.tex`, `.pdf`, and support copy/stdout |
| 3   | Cover Letter Generator | Generate `.txt`, `.pdf` from LLM and convert     |
| 4   | Memory CRUD (`fill`)   | Full user profile editing from CLI               |
| 5   | Logging System         | Log each session to `planc_log.csv`              |
| 6   | Utilities & Status     | status, clear, debug, zip, reapply               |
| 7   | Testing & Polish       | Final testing, UX refinement, docs               |

---

## License

MIT

---

## Author

Swapnil Deb
