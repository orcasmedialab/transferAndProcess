# SCP + Remote Command Automation

This script automates the transfer and processing of PDF files between a Windows and Ubuntu system via SCP and SSH.

## What It Does

1. Transfers all `.pdf` files from a specified local folder to a remote Ubuntu folder
2. Moves transferred files to a local archive directory
3. Runs one or more commands for each file remotely (e.g., to print)
4. Moves the file on the remote machine to a “processed” folder

## Configuration

Edit `config.json` with the following:

- `local_new`: Local folder with new files (absolute path)
- `local_transferred`: Where transferred files should be archived locally
- `remote_unprocessed`: Folder on remote machine to receive files
- `remote_processed`: Remote archive folder
- `remote_host`: SSH host (e.g., `john@10.0.0.0`)
- `commands`: List of shell commands to run remotely, one per file  
  Use `[filename]` as a placeholder for the actual file name  
  Lines starting with `#` will be ignored

## Requirements

- Python 3
- SSH key-based login between local and remote machine
- SCP/SSH available in system path

## Example

To print PDF files remotely:

```json
"commands": [
  "echo Processing [filename]".
  "# pdfinfo [filename] | grep Pages"
]
