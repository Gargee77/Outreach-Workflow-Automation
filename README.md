# Automation Workflow

Tired of copy-pasting the same email 400 times. Built this instead.

Reads a spreadsheet of contacts, generates a draft of the personalized cold email I wrote for each one using a Markdown template + per-company YAML files, and saves them as Gmail drafts. When you're ready, one command sends them all.

## How it works

Each company gets a YAML file with a subject line and a body paragraph. The main template (`email_body.md`) handles the shared structure. The script merges them, converts Markdown to HTML so bold and links work, attaches a file, and saves a draft via the Gmail API. Your Gmail signature is pulled automatically and appended.

Sending is a separate step: `send_drafts.py` asks you to type "send" before anything goes out.

## Setup

**1. Gmail API**

- Create a project at [console.cloud.google.com](https://console.cloud.google.com)
- Enable the Gmail API
- Create OAuth credentials (Desktop app) → download as `credentials.json` in the project root
- Under Audience → Test users, add your Gmail address

**2. Install dependencies**

```
pip install openpyxl pyyaml markdown2 google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**3. Configure**

Edit `config.yml`:
```yaml
resume_path: attachments/your_resume.pdf
```

Drop your resume in `attachments/`.

**4. Write your email template**

Edit `email_body.md`. Three placeholders:
- `{{first_name}}` — pulled from the spreadsheet
- `{{company_body}}` — pulled from the company's YAML
- `{{email_signature}}` — your Gmail signature, fetched automatically

**5. Add a company**

Create `companies/CompanyName.yml` (see `companies/Example.yml`):
```yaml
subject: "Your subject line"
body: |
  Your company-specific paragraph. Supports **bold** and [links](https://example.com).
```

**6. Add recipients**

Spreadsheet with columns: `company`, `full_name`, `email`. The company value should match your YAML filename exactly.

## Usage

Create drafts:
```
python main.py --file your_recipients.xlsx
```

Send when ready:
```
python send_drafts.py
```

`send_drafts.py` matches drafts against your recipients list before sending, so other drafts in your mailbox are untouched. Failed draft IDs are saved to `draft_ids.json` for retry.
