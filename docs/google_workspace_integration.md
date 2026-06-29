# Google Workspace Integration Guide

This guide explains how to connect your AI agents and Python helper scripts with **Google Workspace (Sheets, Docs, Slides, and Gmail)**. This allows you to visually manage client trackers and templates in Google Drive while the agent reads, updates, and creates them dynamically.

---

## 1. Business Gmail vs. Personal Account
*   **Recommendation**: Use a dedicated **Business Google Workspace Account** (e.g. `you@yourconsultancy.com`).
*   **Why?**:
    *   **Scope Isolation**: Keeps your personal documents and emails completely private. The agent only has access to files you explicitly share with it.
    *   **Security**: Prevents accidental leakage of personal data.
    *   **Professionalism**: Outbound emails sent via Gmail API will use your official business address.

---

## 2. Integration Architecture: Google Service Account
The most secure and automated way to link Python scripts or GitHub Actions to Google Workspace is through a **Google Cloud Service Account** (a bot account with its own email address).

```
[GitHub Actions / Local Agent] 
       │ (uses service_account_key.json)
       ▼
 [Google API Client]
       │ (reads/writes authorized files)
       ▼
 [Google Sheets / Drive / Slides]
```

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `consultancy-agent-hub`).

### Step 2: Enable APIs
In the Google Cloud API Library, enable the following APIs:
*   **Google Sheets API** (for trackers, financials, lead logs)
*   **Google Drive API** (for file storage, folder organization)
*   **Google Docs API** (for agreement drafting and proposal documents)
*   **Google Slides API** (for building presentation decks)
*   **Gmail API** (if you want the agent to read/send emails)

### Step 3: Create a Service Account & Generate Key
1. In Cloud Console, go to **IAM & Admin** > **Service Accounts**.
2. Click **Create Service Account**, give it a name (e.g. `workspace-agent`), and click create.
3. Click on the created service account, go to the **Keys** tab, click **Add Key** > **Create New Key**, and select **JSON**.
4. A JSON file containing credentials (e.g. `service-account-key.json`) will download. 
5. **CRITICAL**: Save this file in this repository as `admin/finances/google_creds.json`. It is already protected by our `.gitignore` rules, so it will never be pushed to GitHub.

---

## 3. How to Connect Individual Sheets & Folders
Because the Service Account has its own email (e.g., `workspace-agent@consultancy-agent-hub.iam.gserviceaccount.com`), you can control exactly what it can access:

1.  Create a Google Sheet (e.g., "Consultancy Invoice Log & Tracker") or a Google Drive Folder (e.g., "Clients") on your business account.
2.  Click **Share** in the top right corner.
3.  Add the Service Account's email address as an **Editor**.
4.  The agent can now read and write to this specific folder or sheet using the Python helper scripts.

---

## 4. Script Blueprint (Python Client)
We can write Python utilities using the official `google-api-python-client` library.

### Installation
```bash
pip install google-api-python-client google-auth
```

### Reading/Writing to Sheets (Example Snippet)
```python
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account key
SERVICE_ACCOUNT_FILE = 'admin/finances/google_creds.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build Sheets service
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Write row to a spreadsheet
SPREADSHEET_ID = 'your-google-sheet-id'
RANGE_NAME = 'Sheet1!A1'
values = [["INV-001", "2026-06-20", "Acme Corp", "£4,050.00"]]
body = {'values': values}

result = sheet.values().append(
    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
    valueInputOption='RAW', body=body).execute()
```

---

## 5. What Else Is Needed?
To fully automate operations like building decks (Google Slides) and client agreements:
1.  **Google Slides Templates**: Design a slide deck template (with a consistent style guide, branding, and placeholders like `{{ PROPOSAL_TITLE }}`) on your Google Drive. We can write scripts to clone this template and populate slides with client-specific text.
2.  **Gmail OAuth2 (optional)**: Sending email from a service account can sometimes trigger spam filters. To send emails natively as *you* (rather than the bot email), we can configure **OAuth2 User Consent** in Google Cloud, or use an **App Password** for your business email.
