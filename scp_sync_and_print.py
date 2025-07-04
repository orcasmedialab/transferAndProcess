#!/usr/bin/env python3

import os
import time
import yaml
import subprocess
from pathlib import Path

# Load configuration
CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

local_new = Path(config["local_new"])
local_transferred = Path(config["local_transferred"])
remote_unprocessed = config["remote_unprocessed"]
remote_processed = config["remote_processed"]
remote_host = config["remote_host"]  # e.g., "john@10.0.0.0"
commands = [cmd for cmd in config["commands"] if not cmd.strip().startswith("#") and cmd.strip()]

# Validate directories
for path in [local_new, local_transferred]:
    if not path.exists():
        print(f"[ERROR] Local path does not exist: {path}")
        exit(1)

# Get list of PDF files in local_new
files_to_transfer = list(local_new.glob("*.pdf"))

for file in files_to_transfer:
    dest_local = local_transferred / file.name
    remote_file_check = f"test -f {remote_unprocessed}/{file.name}"

    # Check for local conflict
    if dest_local.exists():
        print(f"[SKIP] File already exists in transferred folder: {dest_local.name}")
        continue

    # Check for remote conflict
    result = subprocess.run(["ssh", remote_host, remote_file_check], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"[SKIP] File already exists in remote unprocessed folder: {file.name}")
        continue

    print(f"Transferring: {file.name}")

    # SCP to remote unprocessed folder
    remote_path = f"{remote_host}:{remote_unprocessed}/"
    scp_cmd = ["scp", str(file), remote_path]
    result = subprocess.run(scp_cmd)

    if result.returncode != 0:
        print(f"[ERROR] SCP failed for {file.name}")
        continue  # Skip to next file

    # Move file locally to 'transferred'
    file.rename(dest_local)
    print(f"Moved to transferred: {dest_local}")

# Now SSH into remote machine to process files
for file_name in [f.name for f in files_to_transfer]:
    remote_file_path = f"{remote_unprocessed}/{file_name}"
    remote_processed_check = f"test -f {remote_processed}/{file_name}"

    # Check if file already exists in remote processed folder
    result = subprocess.run(["ssh", remote_host, remote_processed_check], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"[SKIP] File already exists in remote processed folder: {file_name}")
        continue

    for command_template in commands:
        command = command_template.replace("[filename]", remote_file_path)
        remote_command = f"{command}"
        full_ssh_command = ["ssh", remote_host, remote_command]

        print(f"Running remote command: {remote_command}")
        result = subprocess.run(full_ssh_command)

        if result.returncode != 0:
            print(f"[ERROR] Command failed: {remote_command}")
            continue  # Could also break or log to file if needed

        time.sleep(5)
        print(f"Success: {file_name}")

    # Move the file on remote to processed
    move_cmd = f"mv {remote_file_path} {remote_processed}/{file_name}"
    subprocess.run(["ssh", remote_host, move_cmd])
    print(f"Moved {file_name} to processed folder on remote")
