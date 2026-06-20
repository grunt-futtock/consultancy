#!/usr/bin/env python3
import os
import sys
import json
import csv
from datetime import datetime

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from config: {e}")
        sys.exit(1)

def render_template(template_content, context):
    rendered = template_content
    # Replace all simple context keys
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"
        rendered = rendered.replace(placeholder, str(value))
    return rendered

def log_invoice_to_csv(finance_dir, invoice_data):
    csv_path = os.path.join(finance_dir, "invoice_log.csv")
    headers = ["Invoice Number", "Issue Date", "Due Date", "Client", "Amount", "Status"]
    
    file_exists = os.path.exists(csv_path)
    
    # Extract amount from total_due (strip currency symbols if present)
    amount_str = str(invoice_data.get("TOTAL_DUE", "0.00"))
    
    row = [
        invoice_data.get("INVOICE_NUMBER", "N/A"),
        invoice_data.get("ISSUE_DATE", datetime.now().strftime("%Y-%m-%d")),
        invoice_data.get("DUE_DATE", "N/A"),
        invoice_data.get("CLIENT_NAME", "N/A"),
        amount_str,
        invoice_data.get("STATUS", "Sent")
    ]
    
    try:
        with open(csv_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)
        print(f"  Logged invoice to admin/finances/invoice_log.csv")
    except Exception as e:
        print(f"Warning: Could not log invoice to CSV: {e}")

def main(config_path, client_slug):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    template_path = os.path.join(base_dir, "admin", "templates", "invoice_template.md")
    
    if not os.path.exists(template_path):
        print(f"Error: Invoice template not found at {template_path}")
        sys.exit(1)
        
    # Load config data
    context = load_config(config_path)
    
    # Read template
    with open(template_path, 'r') as f:
        template_content = f.read()
        
    # Render template
    rendered_content = render_template(template_content, context)
    
    # Establish destination paths
    client_dir = os.path.join(base_dir, "clients", client_slug)
    if not os.path.exists(client_dir):
        print(f"Warning: Client directory clients/{client_slug} does not exist. Creating it.")
        os.makedirs(os.path.join(client_dir, "deliverables"), exist_ok=True)
        
    invoice_num = context.get("INVOICE_NUMBER", "Draft")
    filename = f"invoice_{invoice_num}.md"
    dest_path = os.path.join(client_dir, "deliverables", filename)
    
    # Write rendered file
    with open(dest_path, 'w') as f:
        f.write(rendered_content)
        
    print(f"Invoice successfully generated:")
    print(f"  Path: clients/{client_slug}/deliverables/{filename}")
    
    # Log the invoice to the central finances spreadsheet
    finance_dir = os.path.join(base_dir, "admin", "finances")
    os.makedirs(finance_dir, exist_ok=True)
    log_invoice_to_csv(finance_dir, context)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_invoice.py <path_to_json_config> <client_slug>")
        print("Example: python generate_invoice.py new_invoice.json client-abc")
        sys.exit(1)
        
    main(sys.argv[1], sys.argv[2])
