# Termux Cloud Backup for Google Drive (`agy-backup`)

[![Platform](https://img.shields.io/badge/Platform-Android%20Termux-brightgreen)](https://termux.dev)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Storage](https://img.shields.io/badge/Cloud-Google%20Drive%20v3-orange)](https://developers.google.com/drive)

A universal, high-performance, pure-Python cloud backup & restoration tool engineered specifically for **Android Termux**. It provides **universal CLI agent configuration**, **an interactive directory manager**, **custom storage folder additions**, **incremental update sync**, and **Google Drive OAuth2 authentication** for your **AGY CLI**, **Gemini CLI**, **Hermes CLI**, **Termux user environment**, and custom project storage folders.

---

## 🌟 Universal Features & Capabilities

- ⚙️ **Universal Interactive Configuration (`agy-backup config`)**: Interactive setup wizard allowing users to enable/disable specific CLI agent clients (AGY, Gemini CLI, Hermes, etc.), toggle Termux system data, or manage custom storage directories.
- 📁 **Interactive Directory Manager**:
  - `agy-backup add-dir <path>`: Add any custom local folder or project directory (e.g. `/sdcard/Documents`, `~/projects`).
  - `agy-backup remove-dir <path>`: Easily remove custom directory targets.
  - `agy-backup list-dirs`: Display all tracked directories and active client targets.
- 🔄 **Incremental Update Sync**: Uses SHA256 file manifest tracking (`backup_manifest.json`) to detect file changes. If no files changed, it skips redundant uploads. If files changed, it updates the existing cloud file instance rather than creating duplicate files.
- 📁 **Manual Local Directory Options**: Allows exporting/syncing backup archives to local folders (e.g., SD card, shared storage, or custom local directories).
- 🚫 **Smart Exclusions**: Automatically excludes heavy binary caches (`.cache`, `node_modules`), temporary logs (`cli.log`), and Android shared storage mounts (`storage/`, `store/`, `downloads/`, `shared/`) to keep backup archives lightweight and fast.
- 🔑 **Headless Google Drive OAuth2**: Native OAuth2 Device Authorization Flow (`RFC 8628`), perfectly suited for terminal environments without desktop browser requirements.
- 🎯 **Multi-Target Backup Selector**:
  - `agy`: AGY CLI database (`~/.gemini/antigravity-cli`)
  - `gemini`: Gemini CLI databases (`~/.gemini`)
  - `hermes`: Hermes Agent CLI (`~/.hermes`)
  - `termux`: Termux user environment (`~`)
  - `custom_*`: User-added custom storage directories
  - `all`: All active targets combined.
- 🛡️ **Safety-First Restoration**: Automatically creates a local pre-restore snapshot (`~/.gemini/antigravity-cli.pre-restore.bak`) and verifies SHA256 checksums before extracting archives.

---

## 🛠️ Interactive Configuration & Directory Manager Guide

### 1. Run the Universal Configuration Wizard
```bash
agy-backup config
```
*Allows toggling CLI clients (AGY, Gemini, Hermes, Termux) and adding/removing custom directories.*

### 2. Add Custom Storage Directories
Add any custom folder on your phone or Termux filesystem to the cloud backup list:
```bash
# Add a project folder
agy-backup add-dir ~/AGY

# Add a shared phone folder
agy-backup add-dir /sdcard/Documents/Notes
```

### 3. List All Configured Targets & Directories
```bash
agy-backup list-dirs
```

### 4. Remove a Custom Storage Directory
```bash
agy-backup remove-dir Notes
```

---

## 📖 User Guide & Command Reference

### `agy-backup backup`
Perform incremental update sync for active target components or custom directories.

```bash
# Sync all active targets & custom storage directories to Google Drive
agy-backup backup --target all

# Sync only AGY CLI user data
agy-backup backup -t agy

# Sync to Google Drive AND save a copy to a manual local directory
agy-backup backup -t all -l ~/storage/downloads/Backups

# Perform a local-only backup (skip cloud upload)
agy-backup backup -t termux -l ~/manual_backups --local-only

# Force a re-backup even if no file changes were detected
agy-backup backup -t all --force
```

---

### `agy-backup restore`
Safely restore user data from Google Drive or a local archive.

```bash
# Restore latest AGY backup from Google Drive
agy-backup restore -t agy

# Restore specific backup by File ID or List Index #
agy-backup restore -t agy 1

# Restore directly from a local backup archive file
agy-backup restore -t gemini --local-file ~/manual_backups/gemini_backup_latest.tar.gz
```

---

### `agy-backup rollback`
Perform an emergency rollback to the pre-restore local safety snapshot.

```bash
agy-backup rollback
```

---

### `agy-backup status`
View target paths, active CLI agents, credentials status, token validity, and local snapshot state.

```bash
agy-backup status
```

---

## ⏰ Cron & Automated Scheduled Backups

### Method A: Standard Termux Cron (`crontab`)
```bash
pkg install cronie
crontab -e
```
Add line (Runs daily at 2:00 AM):
```cron
0 2 * * * /data/data/com.termux/files/usr/bin/agy-backup backup --target all > /dev/null 2>&1
```

### Method B: Android Job Scheduler (`termux-job-scheduler`)
```bash
termux-job-scheduler \
  --job-id 101 \
  --script "$PREFIX/bin/agy-backup backup --target all" \
  --period-ms 86400000 \
  --charging true \
  --net-connected true
```

---

## 📄 License
Released under the [MIT License](LICENSE).
