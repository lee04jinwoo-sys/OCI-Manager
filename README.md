# OCI-Manager (Oracle Cloud Infrastructure) ☁️

A sleek and powerful CLI tool to manage your Oracle Cloud Infrastructure (OCI) instances, specifically optimized for **Oracle Always Free** ARM instances. This tool provides an interactive TUI (Terminal User Interface) to monitor, manage, and deploy to your cloud servers without leaving the terminal.

## ✨ Key Features

### 1. Real-time Instance Dashboard
*   **Interactive Table**: View all your instances, their status (Running/Stopped), Public IPs, and hardware specs (OCPU, RAM) at a glance.
*   **Always Free Tracking**: Monitor your resource usage against the 4 OCPU and 24GB RAM free tier limits.
*   **Billing Overview**: Check your current monthly accumulated costs.

### 2. Smart SSH Management
*   **Auto-Key Discovery**: Scans common locations (like `.Trash` or `Downloads`) for SSH keys (`.key`, `.pem`) and organizes them into `data/keys` with correct permissions.
*   **One-Touch Connection**: Connect to any instance by simply choosing its number—no need to remember IP addresses.
*   **Auto-User Discovery**: Automatically tests for default users (`ubuntu`, `opc`) and remembers the successful one.

### 3. Remote Execution & Deployment
*   **Bulk Command Execution**: Run shell commands across single or all (`ALL`) instances simultaneously.
*   **File Deployment**: Upload local files/scripts to multiple servers in one go via SFTP.

### 4. Integration & Notifications
*   **Telegram Bot**: Receive notifications and test messages directly to your Telegram account.

## 🛠 Project Structure

```text
Oracle/
├── oci-manager/         # Main Application Source
│   ├── main.py          # Entry point (TUI Dashboard)
│   ├── core/            # Instance & Billing logic
│   ├── ssh/             # Key management & SSH connectors
│   ├── deploy/          # Remote command & SFTP execution
│   └── ui/              # Rich-based UI components
├── list_instances.py    # Lightweight standalone instance lister
└── data/                # (Ignored) Keys, logs, and state storage
```

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Oracle Cloud Account with [OCI CLI configured](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) (`~/.oci/config`).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/lee04jinwoo-sys/OCI-Manager.git
    cd OCI-Manager
    ```
2.  Set up virtual environment & Install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r oci-manager/requirements.txt
    ```
3.  Configure environment variables:
    ```bash
    cp oci-manager/.env.template oci-manager/.env
    # Edit .env with your Telegram token and other settings
    ```

### Usage
Run the main dashboard:
```bash
python oci-manager/main.py
```

## 📄 License
This project is for personal educational use.
