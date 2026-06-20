#!/usr/bin/env python3
import os
import sys
import shutil

def sanitize_client_name(name):
    # Sanitize the client name for filesystem usage (lowercase, hyphenated)
    sanitized = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in name)
    sanitized = sanitized.strip().lower().replace(' ', '-')
    while '--' in sanitized:
        sanitized = sanitized.replace('--', '-')
    return sanitized

def create_client_structure(client_name):
    if not client_name:
        print("Error: Client name cannot be empty.")
        sys.exit(1)
        
    sanitized_name = sanitize_client_name(client_name)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    client_dir = os.path.join(base_dir, "clients", sanitized_name)
    templates_dir = os.path.join(base_dir, "admin", "templates")
    
    print(f"Creating client space for '{client_name}' (directory: clients/{sanitized_name})...")
    
    # Subdirectories to create
    subdirs = [
        "communication",
        "proposals",
        "deliverables"
    ]
    
    for subdir in subdirs:
        path = os.path.join(client_dir, subdir)
        os.makedirs(path, exist_ok=True)
        print(f"  Created directory: clients/{sanitized_name}/{subdir}")
        
    # Copy template files to client directory
    copied_files = []
    
    # Copy agreement template
    agreement_src = os.path.join(templates_dir, "agreement_template.md")
    agreement_dest = os.path.join(client_dir, "proposals", f"agreement_{sanitized_name}.md")
    if os.path.exists(agreement_src):
        shutil.copy2(agreement_src, agreement_dest)
        copied_files.append(f"proposals/agreement_{sanitized_name}.md")
        
    # Copy proposal template
    proposal_src = os.path.join(templates_dir, "proposal_template.md")
    proposal_dest = os.path.join(client_dir, "proposals", f"proposal_{sanitized_name}.md")
    if os.path.exists(proposal_src):
        shutil.copy2(proposal_src, proposal_dest)
        copied_files.append(f"proposals/proposal_{sanitized_name}.md")
        
    # Create a blank meeting log
    meeting_log_path = os.path.join(client_dir, "communication", "meeting_notes.md")
    if not os.path.exists(meeting_log_path):
        with open(meeting_log_path, 'w') as f:
            f.write(f"# Meeting Notes: {client_name}\n\n")
            f.write("## [Date] - Kickoff / Alignment Meeting\n\n")
            f.write("### Attendees\n- Consultant\n- Client Representatives\n\n")
            f.write("### Discussion Topics\n- \n\n")
            f.write("### Action Items\n- [ ] \n")
        copied_files.append("communication/meeting_notes.md")
        
    print("\nInitialization Complete!")
    print(f"New client workspace ready in: clients/{sanitized_name}")
    print("Files created/copied:")
    for f in copied_files:
        print(f"  - clients/{sanitized_name}/{f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_client.py <client_name>")
        sys.exit(1)
        
    client_name_arg = " ".join(sys.argv[1:])
    create_client_structure(client_name_arg)
