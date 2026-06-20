# Consultancy Business Hub

Welcome to the central operations repository for your sole trader consultancy business. This hub integrates strategic business administration, client logs, legal and finance tracking, and client/internal code deliverables.

---

## Directory Layout

*   **`/admin`**: Business operations, finances, and legal templates.
    *   `/templates`: Reusable markdown files for agreements, invoices, and proposals.
    *   `/finances`: Invoice logs (`invoice_log.csv`) and financial tracking. (Git-ignored for privacy).
    *   `/legal`: Registration records and templates. (Git-ignored).
*   **`/clients`**: Client-specific communications, proposals, and deliverables. Folders are slug-case (e.g., `/clients/acme-corp/`).
*   **`/projects`**: Software repositories and automated utilities.
    *   `/internal`: Scripts for internal business automation (e.g. agent helper tools).
    *   `/client-projects`: Technical code built for client accounts.
*   **`/docs`**: General consulting playbooks, tech stack configurations, and founder context logs.

---

## Core Operational Workflows

AI agents and the founder can leverage local command-line tools to automate routine tasks:

### 1. Client Onboarding
To onboard a new client, run the `create_client.py` script:
```bash
python projects/internal/agent-helper/create_client.py "Client Name"
```
This automatically initializes the client folder layout, copies renamed proposal and agreement templates, and starts a meeting log.

### 2. Invoice Generation & Tracking
To generate an invoice and log it to the financial tracker:
1.  Draft a JSON configuration file (e.g. `invoice_config.json`) containing billing rates, hours, invoice IDs, and client details.
2.  Run the `generate_invoice.py` script:
    ```bash
    python projects/internal/agent-helper/generate_invoice.py path/to/invoice_config.json client-slug
    ```
    This creates a markdown invoice in the client's deliverables folder and appends the entry to `admin/finances/invoice_log.csv`.

---

## AI Agent Instructions & Self-Maintenance

When acting as an AI assistant in this repository, you **MUST** adhere to the following rules:

1.  **Alwaysdiscuss and plan** folder layouts, operational workflows, and major changes with the user before executing.
2.  **Maintain data privacy**: Never commit sensitive CSV trackers, API keys, or signed agreements containing Client PII. Ensure `.gitignore` is updated accordingly.
3.  **Self-Maintenance Directive**: If you make any changes to directory structures, add new tools, or modify operational workflows, you **MUST** update this `README.md` and [gemini.md](file:///Users/Rhys_1/development/Consultancy/gemini.md) immediately to reflect the changes. Keep documentation as a live, accurate representation of the repository.
