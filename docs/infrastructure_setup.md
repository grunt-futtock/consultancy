# Infrastructure & Remote Setup Guide

This document explains how to set up two core workflows to allow you to run and access your business systems remotely with zero or minimal hosting costs:
1.  **Mobile Agent Trigger**: Triggering repository automations from your phone via GitHub Actions + Google AI Studio's free tier API.
2.  **Mac Remote Control**: Securing remote SSH/VNC access to your Mac when you are away or the lid is closed.
3.  **LinkedIn Lead Generation Scraping**: Core strategy for scraping prospective client contacts.

---

## 1. Mobile Agent Trigger (GitHub Actions + Google AI Studio)

### Concept
You can command your agent remotely from the official GitHub Mobile app on your phone. 
- You open a **GitHub Issue** in this repository containing your instructions.
- A **GitHub Actions Workflow** detects the issue, triggers a Python script that parses the instructions, and passes it to the Gemini API (Google AI Studio Free Tier).
- The Gemini agent executes the task (e.g. calls `create_client.py` or `generate_invoice.py`), commits the changes, and closes the issue.

### Step 1: Get a Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API Key** and create a key.
3. Save it. (The free tier permits up to 15 Requests Per Minute and 1,500 Requests Per Day, which is plenty for admin tasks).

### Step 2: Add Secret to GitHub
1. In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name: `GEMINI_API_KEY`, Value: *Your API Key*.

### Step 3: Create GitHub Action Workflow File
Save this file as `.github/workflows/mobile_agent.yml`:

```yaml
name: Mobile Agent Assistant

on:
  issues:
    types: [opened]

jobs:
  run-agent:
    if: startsWith(github.event.issue.title, '[Agent]')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-python: '3.10'

      - name: Install dependencies
        run: |
          pip install google-generativeai

      - name: Execute Agent script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          ISSUE_TITLE: ${{ github.event.issue.title }}
          ISSUE_BODY: ${{ github.event.issue.body }}
        run: |
          python projects/internal/agent-helper/run_mobile_agent.py

      - name: Commit changes
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add .
          git diff --quiet && git diff --staged --quiet || (git commit -m "Agent: Executed mobile instruction" && git push)
```

---

## 2. Remote Access to your Mac (Tailscale + SSH/VNC)

To access your actual macOS development environment when you're out or on your couch:

### Step 1: Install Tailscale (VPN)
**Tailscale** creates a private, encrypted mesh network between your devices with zero configuration. It avoids opening any ports on your home router.
1. Download and install Tailscale on your **Mac** and your **Phone/Tablet**.
2. Log in using the same account.
3. Your Mac will receive a stable, private IP address (e.g. `100.x.y.z`).

### Step 2: Enable Remote Services on macOS
1. On your Mac, open **System Settings** > **General** > **Sharing**.
2. Toggle on **Remote Login** (enables SSH).
3. Toggle on **Remote Management** or **Screen Sharing** (enables VNC).

### Step 3: Prevent Mac Sleeping with Closed Lid
By default, closing a Mac lid puts it to sleep.
*   **Software Solution**: Install **Amphetamine** (Free on macOS App Store) and configure it to "Keep awake when lid is closed" (requires Mac to be connected to power).
*   **Terminal command**: Run `caffeinate -d` in the terminal to prevent sleep, though Amphetamine provides a safer UI.

### Step 4: Connecting from your Phone
*   **CLI / SSH Access**: Use **Termius** or **Blink Shell** on iOS/Android. Connect to the Tailscale IP of your Mac (e.g. `ssh username@100.x.y.z`).
*   **GUI / Screen Access**: Download **VNC Viewer** (RealVNC) or Screens on your phone. Connect to the Mac's Tailscale IP address to view and control your desktop.

---

## 3. Model Context Protocol (MCP) Integration

Model Context Protocol (MCP) is an open standard that allows LLMs and AI clients (like Claude Desktop, Cursor, or Cline/Roo Code) to connect to external databases, APIs, and local terminal/file utilities securely. This is a game-changer for solo consulting.

### Recommended MCP Servers to Install
1.  **Local Filesystem Server**: Exposes local file read/write operations. Usually built into advanced editor plugins (such as Cline/Roo Code) or run via Node: `@modelcontextprotocol/server-filesystem`.
2.  **GitHub MCP Server**: Connects to the GitHub API. Allows agents to create branch PRs, search repository files, and manage issues directly from your chat client: `github.com/modelcontextprotocol/servers/tree/main/src/github`.
3.  **Google Sheets MCP Server**: Allows your agent to write revenue, invoice tracking lines, or leads directly to Google Sheets for easier sharing and reporting: `github.com/modelcontextprotocol/servers/tree/main/src/google-sheets`.
4.  **Database (PostgreSQL/SQLite) MCP Server**: Allows agents to run SQL analytics queries against local or remote databases: `github.com/modelcontextprotocol/servers/tree/main/src/postgres`.
5.  **Custom Agency MCP Server**: You can build a small custom Python server using the `mcp` SDK to expose your custom tools (e.g. `create_client` and `generate_invoice`) directly as native tool calls to any AI client.

---

## 4. Git Hosting & Repository Architecture

To run a secure, zero-cost operations center, we recommend sticking to the following Git hosting parameters:

### GitHub Free Tier (Recommended)
*   **Benefits**: Private repositories, 2,000 free GitHub Actions run-minutes/month, issue boards for mobile tasking, and native markdown rendering for invoices/contracts.
*   **Actions Security**: Configure environments with branch protection rules so that Actions cannot push code changes to `main` without checking lint rules, protecting against agent bugs.

### Husky & Pre-commit Hooks
To prevent commits containing placeholders (like `{{ CLIENT_NAME }}`) from accidentally leaking into main:
1.  Initialize `husky` in the repository.
2.  Set a pre-commit hook that checks if any markdown file under `clients/` contains unrendered braces (`{{` or `}}`) and blocks the commit if found.

---

## 5. LinkedIn Lead Generation Scraper Strategy

To automate finding prospects on LinkedIn without triggering anti-scraping blocks:

### Recommended Approach: Third-Party APIs
Scraping LinkedIn directly using Selenium or BeautifulSoup often results in account restrictions due to strict detection. The safest way is using specialized proxy scraper APIs (e.g. via RapidAPI) which are cheap (e.g. $10 for 10,000 requests) and bypass blocks.

### Lead Generation Pipeline Design
1.  **Search Input**: Search term (e.g. "Growth Director", "eCommerce Founder" + Location).
2.  **Scraper Utility**: Python script calling a RapidAPI LinkedIn Scraper to fetch company profiles, names, and titles.
3.  **Filter Logic**: Discard companies with internal software development teams (likely won't need vibe-coding support). Keep companies with marketing operations but small engineering counts.
4.  **Logging**: Write prospective leads to `docs/leads_tracker.csv`.

*A starter implementation for the lead generator script can be written in `projects/internal/lead-gen/scrape_linkedin.py` when you are ready to begin targeting.*
