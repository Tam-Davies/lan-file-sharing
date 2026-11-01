# LAN File Sharing

A lightweight, responsive web-based file-sharing application for devices connected to the same local network.

The application runs on a host computer and allows other devices on the same Wi-Fi/LAN to access shared files through a web browser.

## Features

- 📁 Upload files from the server
- 📥 Download shared files from connected devices
- 🎥 Supports video files and other common file types
- 🗂️ Shared file library
- 📊 File-sharing activity history
- 🌐 Access from other devices on the same LAN
- 📱 Responsive mobile-friendly interface
- ☀️ Light and dark mode
- ☰ Responsive hamburger navigation on smaller screens
- 🗄️ SQLite database for activity tracking
- 🔒 Server-only upload functionality
- ⚡ Lightweight Flask backend

---

## Architecture

```text
                    Local Wi-Fi / LAN
                           │
                           │
                    ┌──────▼──────┐
                    │    Server   │
                    │   Flask App │
                    │   Port 5000 │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        shared_files/   SQLite DB    Web Interface
              │        history.db          │
              │                            │
       ┌──────┴───────┐              ┌─────┴─────┐
       │              │              │           │
       ▼              ▼              ▼           ▼
     Laptop         Phone         Tablet      Desktop
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework |
| SQLite | Activity/history database |
| HTML | Web interface |
| CSS | Responsive UI and themes |
| JavaScript | Interactivity |
| WSL | Development environment |
| Windows Port Proxy | LAN access to Flask running in WSL |

---

## Project Structure

```text
lan-file-sharing/
│
├── app.py
│
├── shared_files/
│   └── uploaded files
│
├── database/
│   └── history.db
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd lan-file-sharing
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Flask

```bash
pip install flask
```

---

# Running the Application

Start the Flask server:

```bash
python app.py
```

The application runs on:

```text
http://127.0.0.1:5000
```

For LAN access, Flask should listen on:

```text
0.0.0.0:5000
```

---

# LAN Access

Because the project is running inside WSL, Windows can expose the Flask application to other devices using a port proxy.

Example:

```powershell
netsh interface portproxy add v4tov4 `
listenaddress=172.20.10.2 `
listenport=5000 `
connectaddress=172.19.81.167 `
connectport=5000
```

The IP addresses above are examples and may change depending on the network and WSL configuration.

Check the current port proxy:

```powershell
netsh interface portproxy show all
```

Other devices connected to the same Wi-Fi can then access the application using the Windows LAN IP:

```text
http://<WINDOWS-LAN-IP>:5000
```

Example:

```text
http://172.20.10.2:5000
```

---

# Windows Firewall

If other devices cannot connect, allow TCP port `5000` through Windows Firewall:

```powershell
New-NetFirewallRule `
    -DisplayName "LAN File Sharing 5000" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5000 `
    -Action Allow `
    -Profile Any
```

---

# File Upload

Only the server can upload files.

The upload form uses:

```html
<input
    type="file"
    name="file"
    id="file"
>
```

There is no hard-coded restriction to specific extensions.

Files such as:

```text
.mp4
.pdf
.csv
.xlsx
.docx
.png
.jpg
.zip
```

can be uploaded.

After selecting a file, JavaScript updates the upload control to display the selected filename.

Example:

```text
Choose File
```

becomes:

```text
index.mp4
```

---

# Shared Files

Uploaded files are stored in:

```text
shared_files/
```

Example:

```text
shared_files/
├── index.mp4
├── Billing_data.csv
├── IMG_1120.png
└── report.pdf
```

Files can then be downloaded by devices connected to the LAN.

---

# Activity History

The application records file activity in SQLite.

Database location:

```text
database/history.db
```

The history table contains:

```text
id
filename
action
client_ip
timestamp
```

Example:

```text
1 | Billing_data.csv | UPLOAD | 127.0.0.1 | 2026-11-01 17:21:12
```

You can inspect the database with:

```bash
sqlite3 database/history.db
```

Then:

```sql
SELECT * FROM history;
```

---

# User Interface

The interface includes:

### Dashboard

Provides an overview of the file-sharing server and network status.

### Shared Files

Displays files currently available for download.

### History

Displays file upload and download activity.

### Dark Mode

The interface supports light and dark themes.

The selected theme is stored in the browser's local storage.

### Mobile View

On smaller screens, the desktop navigation changes into a hamburger menu:

```text
☰
```

Tapping the menu displays:

```text
Dashboard
Shared Files
History
```

The layout also adapts file cards, statistics, upload controls, and other components for smaller screens.

---

# Security Model

The application is designed for use on a trusted local network.

Current access model:

```text
Server
  │
  ├── Upload
  ├── Download
  └── View History
       │
       ▼
LAN Clients
  │
  ├── Download
  └── View permitted content
```

The application is **not intended to be directly exposed to the public internet**.

For internet-facing deployment, authentication, authorization, HTTPS, input validation, rate limiting, and additional security controls should be implemented.

---

# Testing

## Test the Server Locally

```bash
curl http://127.0.0.1:5000
```

Expected response:

```text
HTTP 200
```

## Test File Upload

Example:

```bash
curl -F "file=@/mnt/c/Users/user/Videos/index.mp4" \
http://127.0.0.1:5000/upload
```

After uploading:

```bash
ls -lh shared_files/
```

The uploaded file should appear.

---

# Development Environment

The project was developed using:

```text
Windows
WSL Ubuntu
Python
Flask
SQLite
VS Code
```

The Flask server runs inside WSL while Windows provides LAN connectivity through port forwarding.

---

# Future Improvements

Potential future versions could include:

- 🔐 User authentication
- 👤 User accounts
- 🔑 Access-controlled shared folders
- 📤 Drag-and-drop uploads
- 📊 File size and storage statistics
- 🔍 File search
- 🗑️ File deletion
- 📁 Folder support
- ⏳ Upload progress indicators
- 🔔 Notifications
- 📱 Improved mobile interface
- 🔒 HTTPS
- 🛡️ File validation and malware scanning
- 🚀 Production deployment with Gunicorn
- 🐳 Docker deployment
- 📡 Automatic LAN server discovery

---

# Project Status

**Status:** Functional MVP

Current capabilities:

```text
✓ Flask backend
✓ SQLite activity tracking
✓ File uploads
✓ File downloads
✓ Video uploads
✓ LAN access
✓ Responsive interface
✓ Mobile navigation
✓ Light/dark mode
✓ Shared file library
✓ Activity history
```

---

## Author

**TammyDX**

Built as a practical LAN networking, Python, Flask, and web-development project.