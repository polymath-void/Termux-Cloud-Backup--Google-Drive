<!--
SEO Title: Termux Cloud Backup for Google Drive - Incremental Sync & Universal CLI Backup Tool
SEO Description: Open-source pure-Python backup and restoration CLI tool for Android Termux. Features incremental Google Drive OAuth2 sync, multi-agent CLI database backup (AGY, Gemini CLI, Hermes), interactive directory manager, and zero-dependency recovery.
SEO Keywords: Termux Google Drive Backup, Android Termux Cloud Backup, Termux Restore Tool, AGY CLI Backup, Gemini CLI Backup, Termux Incremental Sync, Termux OAuth2 Google Drive, Termux Job Scheduler Cron Backup
-->

# Termux Cloud Backup for Google Drive (`agy-backup`)

[![Platform](https://img.shields.io/badge/Platform-Android%20Termux-brightgreen?logo=android)](https://termux.dev)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Cloud API](https://img.shields.io/badge/API-Google%20Drive%20v3-orange?logo=googledrive)](https://developers.google.com/drive)
[![OAuth Protocol](https://img.shields.io/badge/Auth-RFC%208628%20Device%20Flow-red)](https://datatracker.ietf.org/doc/html/rfc8628)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Cite](https://img.shields.io/badge/Cite-BibTeX-purple)](#-citation--attribution)

> **The definitive open-source cloud backup and restoration utility engineered natively for Android Termux.** Features incremental update sync, Google Drive OAuth2 device authorization, interactive directory management, and multi-client database protection for AGY CLI, Gemini CLI, Hermes Agent, and custom Linux/Termux storage paths.

---

## 📌 Table of Contents

- [Overview \& Key Features](#-overview--key-features)
- [System Architecture \& Protocols](#-system-architecture--protocols)
- [Installation \& Quick Start](#-installation--quick-start)
- [Google Drive OAuth2 Authentication](#-google-drive-oauth2-authentication)
- [Universal Interactive Directory Manager](#-universal-interactive-directory-manager)
- [Backup Execution \& Local Export Guide](#-backup-execution--local-export-guide)
- [Step-by-Step Restoration \& Rollback Protocol](#-step-by-step-restoration--rollback-protocol)
- [Automated Cron \& Job Scheduler Workflows](#-automated-cron--job-scheduler-workflows)
- [Smart Exclusion Rules](#-smart-exclusion-rules)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [Citation \& Attribution](#-citation--attribution)
- [License](#-license)

---

## 🚀 Overview & Key Features

`agy-backup` solves the critical challenge of persistent data storage and disaster recovery on non-root **Android Termux** environments. Built with pure Python standard libraries, it eliminates heavy external binary dependencies while delivering enterprise-grade cloud synchronization.

### Core Capabilities

- 🔄 **Incremental Matrix Syncing**: Employs SHA-256 file manifest tracking (`backup_manifest.json`) to calculate delta state changes. When files are unmodified, backup steps are bypassed. When files change, existing Google Drive cloud file instances are patched in-place to prevent cloud clutter.
  
- ⚙️ **Universal CLI Agent Support**: Natively auto-detects and manages databases for **Antigravity AGY CLI** (`~/.gemini/antigravity-cli`), **Gemini CLI** (`~/.gemini`), **Hermes Agent CLI** (`~/.hermes`), and custom Termux environment dotfiles (`~`).
  
- 📂 **Interactive Storage Directory Manager**: Add or remove custom project directories (`agy-backup add-dir <path>`) or shared Android storage folders (`/sdcard/Documents`) on the fly.
  
- 🔑 **RFC 8628 Headless OAuth2**: Implements Google OAuth2 Device Authorization Grant, allowing seamless browser-based authentication without requiring a desktop display server or GUI.
  
- 💾 **Dual Storage Modes**: Sync directly to Google Drive cloud storage or export timestamped tarballs to manual local directory options (e.g. SD cards or external USB storage).
  
- 🛡️ **Fail-Safe Rollback Engine**: Automatically captures a pre-restore local safety snapshot (`~/.gemini/antigravity-cli.pre-restore.bak`) and enforces cryptographic SHA-256 digest validation prior to archive extraction.

---

## 🏗️ System Architecture & Protocols

```
                                +-----------------------------------+
                                |      Android Termux Sandbox       |
                                +-----------------------------------+
                                                  |
           +--------------------------------------+--------------------------------------+
           |                                      |                                      |
           v                                      v                                      v
+-----------------------+              +-----------------------+              +-----------------------+
|  Antigravity AGY CLI  |              |      Gemini CLI       |              |  Custom Storage Dirs  |
| ~/.gemini/antigravity |              |       ~/.gemini       |              |   ~/projects, /sdcard |
+-----------------------+              +-----------------------+              +-----------------------+
           |                                      |                                      |
           +--------------------------------------+--------------------------------------+
                                                  |
                                                  v
                               +------------------------------------+
                               |     SHA-256 Manifest Checksum      |
                               |    (backup_manifest.json Match)    |
                               +------------------------------------+
                                                  |
                                  +---------------+---------------+
                                  |                               |
                         (No Delta Detected)              (Delta Detected)
                                  |                               |
                           [ Skip Sync ]               [ Gzip Tarball Engine ]
                           Zero Bandwidth                         |
                                                    +-------------+-------------+
                                                    |                           |
                                                    v                           v
                                         +--------------------+       +--------------------+
                                         |  Google Drive v3   |       | Local Storage Path |
                                         |   (/AGY_Backups)   |       | (-l /sdcard/...)   |
                                         +--------------------+       +--------------------+
```

### Technical Specifications

| Component | Technical Protocol / Specification |
|---|---|
| **Cloud Storage Protocol** | Google Drive API v3 REST (`https://www.googleapis.com/drive/v3`) |
| **Authentication Standard** | OAuth 2.0 Device Authorization Grant ([RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)) |
| **Archive Compression** | Gzip Tarball (`.tar.gz`) via Python `tarfile` |
| **Digest Integrity** | Cryptographic SHA-256 (`hashlib`) Checksum Verification |
| **Execution Environment** | Android Bionic libc Termux (`aarch64` / `arm64`) |

---

## ⚡ Installation & Quick Start

### Prerequisites
- **OS**: Android Termux (Android 7.0+)
- **Packages**: `python3`, `git`

### Command-Line Setup

```bash
# 1. Install required packages
pkg update && pkg install -y python git

# 2. Clone the official repository
git clone https://github.com/polymath-void/Termux-Cloud-Backup-Google-Drive.git ~/Termux-Cloud-Backup-Google-Drive

# 3. Grant execution permissions & link to binary path
chmod +x ~/Termux-Cloud-Backup-Google-Drive/bin/agy-backup
ln -sf ~/Termux-Cloud-Backup-Google-Drive/bin/agy-backup $PREFIX/bin/agy-backup
termux-fix-shebang $PREFIX/bin/agy-backup

# 4. Verify system status
agy-backup status
```

---

## 🔑 Google Drive OAuth2 Authentication

`agy-backup` uses headless Google OAuth2 authentication. No browser extensions or desktop GUI components are needed.

1. **Obtain Client Credentials**:
   - Navigate to [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials).
   - Click **+ Create Credentials** $\rightarrow$ **OAuth client ID**.
   - Select Application Type: **TVs and Limited Input devices** (or **Desktop app**).
   - Copy your **Client ID** and **Client Secret**.

2. **Execute Interactive Authentication**:
   ```bash
   agy-backup auth
   ```
   - Input your Client ID and Client Secret.
   - Open [https://www.google.com/device](https://www.google.com/device) on your mobile browser or PC.
   - Enter the displayed 8-character verification code to issue your secure access tokens.

---

## 📂 Universal Interactive Directory Manager

Customize which CLI agent databases or system directories are protected.

### Commands

| Command | Action |
|---|---|
| `agy-backup config` | Launch the interactive configuration and target selector wizard |
| `agy-backup add-dir <path>` | Add a custom storage directory or project folder to the backup profile |
| `agy-backup remove-dir <path>` | Remove a custom storage directory from the backup profile |
| `agy-backup list-dirs` | List all active agent clients and custom storage directories |

### Usage Examples

```bash
# Launch interactive configuration wizard
agy-backup config

# Add your coding projects folder
agy-backup add-dir ~/AGY

# Add Android shared Documents folder
agy-backup add-dir /sdcard/Documents/MyNotes

# List all tracked backup paths
agy-backup list-dirs
```

---

## 💻 Backup Execution & Local Export Guide

Execute cloud or local backups using the `backup` subcommand.

```bash
# Perform incremental cloud sync for all active targets & custom folders
agy-backup backup --target all

# Sync only Antigravity AGY CLI database
agy-backup backup -t agy

# Sync to Google Drive AND save a copy to a manual local directory
agy-backup backup -t all -l ~/storage/downloads/Backups

# Offline backup: local directory export only (bypasses cloud upload)
agy-backup backup -t termux -l ~/manual_backups --local-only

# Force re-backup regardless of file modification state
agy-backup backup -t all --force
```

---

## 🛡️ Step-by-Step Restoration & Rollback Protocol

### 1. Restore on a New Phone or Fresh Termux Installation
```bash
# Authenticate & list cloud backups
agy-backup auth
agy-backup list

# Restore targets by list index
agy-backup restore -t agy 1
agy-backup restore -t gemini 1
agy-backup restore -t termux 1
```

### 2. Restore from a Specific Google Drive File ID
```bash
agy-backup restore -t agy 1ldLJJgGFoztb8b6Q3td0Izc40jd8Rx06
```

### 3. Restore from a Local Backup File (`--local-file`)
```bash
agy-backup restore -t agy --local-file ~/manual_backups/agy_backup_latest.tar.gz
```

### 4. Emergency Rollback (`agy-backup rollback`)
If a restoration breaks your local environment, restore the pre-operation safety snapshot:
```bash
agy-backup rollback
```

---

## ⏰ Automated Cron & Job Scheduler Workflows

### Method 1: Standard Termux Crontab (`cronie`)
```bash
pkg install cronie
crontab -e
```
Add the following line to run daily cloud backup sync at 2:00 AM:
```cron
0 2 * * * /data/data/com.termux/files/usr/bin/agy-backup backup --target all > /dev/null 2>&1
```
Start cron daemon: `crond`

### Method 2: Android Native Job Scheduler (`termux-job-scheduler`)
Schedule daily background runs that survive Android battery optimization:
```bash
termux-job-scheduler \
  --job-id 101 \
  --script "$PREFIX/bin/agy-backup backup --target all" \
  --period-ms 86400000 \
  --charging true \
  --net-connected true
```

---

## 🚫 Smart Exclusion Rules

To ensure archives remain compact (< 10 MB) and upload speeds stay fast, the following directories are automatically excluded:

```
storage/        (Android shared storage mount)
store/          (Secondary shared media store)
downloads/      (Uncategorized browser downloads)
shared/         (Shared system media mounts)
.cache/         (Binary package & model caches)
node_modules/   (Heavy npm dependency trees)
cli.log         (Session runtime log streams)
.git/objects/   (Git binary pack files)
```

---

## ❓ Frequently Asked Questions (FAQ)

#### Q1: Does `agy-backup` require root access on Android?
**No.** `agy-backup` operates entirely within the standard non-root Android application sandbox in Termux.

#### Q2: How does incremental update sync work?
`agy-backup` computes cryptographic SHA-256 digests of included files and stores them in `backup_manifest.json`. If no files change between runs, cloud uploads are skipped. When changes occur, the existing remote file ID on Google Drive is patched in-place.

#### Q3: Where are Google OAuth credentials stored?
Credentials and tokens are stored locally in your Termux home directory at `~/.gemini/antigravity-cli/gdrive_credentials.json` and `gdrive_token.json`. They are never transmitted to third-party servers.

#### Q4: Can I back up custom folders outside `~/.gemini`?
**Yes.** Use `agy-backup add-dir /path/to/directory` to add any custom folder or project path to your backup profile.

---

## 📄 Citation & Attribution

If you use `agy-backup` in academic research, developer tooling projects, or technical documentation, please cite this project as follows:

### BibTeX Citation
```bibtex
@software{termux_cloud_backup_2026,
  author       = {Polymath Void and AGY Contributors},
  title        = {Termux Cloud Backup for Google Drive: Incremental Sync Utility for Android Termux},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{https://github.com/polymath-void/Termux-Cloud-Backup-Google-Drive}},
  version      = {1.2.0}
}
```

### APA Style
Polymath Void. (2026). *Termux Cloud Backup for Google Drive: Incremental Sync Utility for Android Termux* (Version 1.2.0) [Computer software]. GitHub. https://github.com/polymath-void/Termux-Cloud-Backup-Google-Drive

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
