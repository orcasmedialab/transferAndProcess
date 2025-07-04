# SCP + Remote Command Automation

This script automates the transfer and processing of PDF files between a local Windows machine and a remote Ubuntu system via SCP and SSH.

## What It Does

1. Transfers all `.pdf` files from a specified local folder to a remote Ubuntu folder
2. Moves transferred files to a local archive directory
3. Runs one or more commands for each file remotely (e.g., to print, rename, or inspect)
4. Moves the file on the remote machine to a "processed" folder

## Configuration

Edit `config.yaml` with the following:

```yaml
local_new: ""             # Local folder with new files
local_transferred: ""     # Local folder for transferred files
remote_unprocessed: ""    # Remote folder to receive files
remote_processed: ""      # Remote folder for processed files
remote_host: ""           # SSH host (e.g., "john@10.0.0.0")
commands:
  - "# Commands that begin with '#' are ignored"
  - "echo Processing [filename]"
  - "# pdfinfo [filename] | grep Pages"
```

- Use `[filename]` as a placeholder for the file name
- Comment out any command you want to disable with `#`

## Requirements

- Python 3
- SSH key-based login between local and remote machine
- `scp` and `ssh` available in your system path
- Optional: `poppler-utils` (for `pdfinfo` or `pdftotext` examples)

## Example Use Cases

Print files, rename them with timestamps, or inspect content:

```yaml
commands:
  - "# Commands that begin with '#' are ignored"
  - "echo Processing [filename]"
  - "# pdfinfo [filename] | grep Pages"
```

## Notes

- Files that fail SCP are skipped
- Remote commands that fail are logged and skipped (but script continues)
- Output is printed to console for transparency
- Commands are issued with a hardcoded 5-second delay from one to the next

## To Run

Make sure your config file is filled out, then run:

```bash
python scp_sync_and_print.py
```

## Future Work
- Declare inter-command sleep duration in config
