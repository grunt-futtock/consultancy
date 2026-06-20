# Repository Context: Consultancy Business Hub

This repository serves as the central hub for a sole trader consultancy business. It is used to manage business operations, client relationships, financial tracking, legal documents, and the technical projects ("vibecoding") developed for clients or internal use.

---

## Business Profile

- **Structure**: Sole Trader (Individual Consultant)
- **Focus Areas**: Software development, technology consulting, and custom programming solutions ("vibecoding").
- **Operating Model**: Direct client engagements, project-based delivery, and ongoing technical support.

---

## Repository Purpose & AI Instructions

When working in this repository, follow these core principles:

1. **Strategic Planning First**: Always discuss and plan folder layouts, operational workflows, and major changes with the user before executing.
2. **Business & Tech Integration**: Maintain a clean separation between administrative business files (clients, finances, legal docs) and technical codebase files (applications, packages, scripts), while ensuring they are easily cross-referenced.
3. **Data Privacy & Security**: Treat all client data, financial logs, and legal files with strict confidentiality. Avoid hardcoding sensitive keys, credentials, or personal identification information (PII).
4. **Iterative Refinement**: Update this `gemini.md` file as the business evolves, adding new operational guidelines, project directories, and tool workflows.

---

## Active Directory Structure

The repository follows a clean separation between business administration, client logs, and client/internal code:

- **`/admin`**: Business operations, finances, legal templates.
  - `/templates`: Reusable markdown files for agreements, invoices, and proposals.
  - `/finances`: Invoice logs (`invoice_log.csv`) and financial tracking. (Git-ignored to protect revenue privacy).
  - `/legal`: Registration records and signed agreements. (Git-ignored to protect PII).
- **`/clients`**: Client-specific communications, proposals, and deliverables. Folders are slug-case (e.g., `/clients/acme-corp/`).
- **`/projects`**: Software repositories and automated utilities.
  - `/internal`: Scripts for internal business automation (e.g., helper tools).
  - `/client-projects`: Technical code and deliverable repositories built for client accounts.
- **`/docs`**: General consulting playbooks, methodology reference sheets, and tech stack configurations.

---

## Agent Operational Workflows

To keep administrative overhead minimal, AI agents can leverage internal scripts for client onboarding and invoice creation:

### 1. Client Onboarding
To onboard a new client, run the `create_client.py` script:
```bash
python projects/internal/agent-helper/create_client.py "Client Name"
```
This automatically:
- Creates `clients/client-name/` structure.
- Copies the agreement and proposal templates to `clients/client-name/proposals/` pre-renamed.
- Creates a blank meeting notes log in `clients/client-name/communication/`.

### 2. Invoicing
To generate an invoice and log it to the financial tracker:
1. Draft a JSON file (e.g. `invoice_config.json`) containing all values for `invoice_template.md` (e.g. `INVOICE_NUMBER`, `ISSUE_DATE`, `DUE_DATE`, `CLIENT_NAME`, `TOTAL_DUE`, and item line descriptions/rates).
2. Run the `generate_invoice.py` script:
   ```bash
   python projects/internal/agent-helper/generate_invoice.py path/to/invoice_config.json client-slug
   ```
3. This creates a markdown invoice in `clients/client-slug/deliverables/invoice_[number].md` and appends the entry to `admin/finances/invoice_log.csv`.

