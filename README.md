# Termux Cloud Backup for Google Drive (`agy-backup`)

[![Platform](https://img.shields.io/badge/Platform-Android%20Termux-brightgreen)](https://termux.dev)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Storage](https://img.shields.io/badge/Cloud-Google%20Drive%20v3-orange)](https://developers.google.com/drive)

A lightweight, high-performance, pure-Python cloud backup & restoration tool engineered specifically for **Android Termux**. It provides **incremental update sync**, **manual local directory options**, and automated **Google Drive OAuth2 authentication** to back up and restore your **AGY CLI**, **Gemini CLI**, and **Termux user environment** databases.

---

## 🌟 Key Features

- 🔄 **Incremental Update Sync**: Uses SHA256 file manifest tracking to detect file changes. If no files changed, it skips redundant uploads. If files changed, it updates the existing cloud file instance rather than creating duplicate files.
- 📁 **Manual Local Directory Options**: Allows exporting/syncing backup archives to local folders (e.g., SD card, shared storage, or custom local directories).
- 🚫 **Smart Exclusions**: Automatically excludes heavy binary caches (`.cache`, `node_modules`), temporary logs (`cli.log`), and Android shared storage mounts (`storage/`, `store/`, `downloads/`, `shared/`) to keep backup archives lightweight and fast.
- 🔑 **Headless Google Drive OAuth2**: Native OAuth2 Device Authorization Flow (`RFC 8628`), perfectly suited for terminal environments without desktop browser requirements.
- 🎯 **Multi-Target Backup Selector**:
  - `agy`: AGY CLI database (`~/.gemini/antigravity-cli`: settings, knowledge, skills, memory, conversations, brain, MCP)
  - `gemini`: Gemini CLI databases (`~/.gemini`: credentials, history, policies, state, project configs)
  - `termux`: Termux user environment (`~`: `.termux`, `.bashrc`, `.zshrc`, `.profile`, `.ssh`, `AGY`, `skills-workspace`)
  - `all`: All component targets combined.
- 🛡️ **Safety-First Restoration**: Automatically creates a local pre-restore snapshot (`~/.gemini/antigravity-cli.pre-restore.bak`) and verifies SHA256 checksums before extracting archives.

---

## 🚫 Directory Exclusions (What is NOT backed up)

To prevent gigabytes of media or transient files from cluttering your cloud backup, the following paths are **strictly excluded**:

| Path / Pattern | Reason for Exclusion |
|---|---|
| `~/storage/`, `~/store/`, `~/downloads/` | Android shared storage mounts (photos, videos, large downloads). |
| `~/.cache/`, `node_modules/` | Temporary package & model binary caches. |
| `cli.log`, `crashes/`, `updater/` | Session runtime logs & temporary update dumps. |
| `*.lock`, `*.tmp` | Active process lock files. |
| `.git/objects/` | Git pack caches (git source code files remain included). |

---

## 📖 Comprehensive Step-by-Step Restoration Guide

### Scenario 1: Restoring on a New Phone / Fresh Termux Install
When setting up a brand-new device:

1. **Install Python & Git**:
   ```bash
   pkg update && pkg install python git
   ```
2. **Clone Repository & Install Tool**:
   ```bash
   git clone https://github.com/polymath-void/Termux-Cloud-Backup-Google-Drive.git ~/Termux-Cloud-Backup-Google-Drive
   chmod +x ~/Termux-Cloud-Backup-Google-Drive/bin/agy-backup
   ln -sf ~/Termux-Cloud-Backup-Google-Drive/bin/agy-backup $PREFIX/bin/agy-backup
   termux-fix-shebang $PREFIX/bin/agy-backup
   ```
3. **Authenticate Google Drive**:
   ```bash
   agy-backup auth
   ```
4. **List & Restore Remote Backups**:
   ```bash
   # See available cloud backups
   agy-backup list

   # Restore all components (AGY CLI, Gemini CLI, Termux environment)
   agy-backup restore -t agy 1
   agy-backup restore -t gemini 1
   agy-backup restore -t termux 1
   ```

---

### Scenario 2: Restoring from a Specific Cloud Backup Version
If you have multiple backups saved in Google Drive:

```bash
# 1. List remote backups to find File IDs or list index numbers
agy-backup list

# Output Example:
# #   Backup Name                      Size (MB)  Created Date         File ID
# 1   agy_backup_latest.tar.gz         1.65       2026-08-03 23:13:21  1ldLJJgGFoztb8b6Q3td0Izc40jd8Rx06
# 2   gemini_backup_latest.tar.gz      0.01       2026-08-03 23:12:59  1yBjLg3FPtu9i0q8HAdC29RxkjTNl9Jgr

# 2. Restore using List Index #
agy-backup restore -t agy 1

# 3. Restore using Google Drive File ID
agy-backup restore -t agy 1ldLJJgGFoztb8b6Q3td0Izc40jd8Rx06
```

---

### Scenario 3: Restoring from a Local Backup File (`--local-file`)
If you stored a backup archive on your SD card or local directory:

```bash
agy-backup restore -t agy --local-file ~/manual_backups/agy_backup_latest.tar.gz
```

---

### Scenario 4: Emergency Local Rollback (`agy-backup rollback`)
Before any restore operation executes, `agy-backup` automatically saves a local pre-restore snapshot at `~/.gemini/antigravity-cli.pre-restore.bak`. If a restoration breaks your configuration:

```bash
agy-backup rollback
```
*This instantly restores your local state prior to the restoration attempt.*

---

## ⏰ Cron & Automated Scheduled Backups

You can set up automated, hands-free cloud backups so your environment is synced daily without manual interaction.

### Method A: Standard Termux Cron (`crontab`)

1. **Install `cronie`**:
   ```bash
   pkg install cronie
   ```
2. **Edit Crontab**:
   ```bash
   crontab -e
   ```
3. **Add Daily Backup Schedule (Runs every night at 2:00 AM)**:
   ```cron
   0 2 * * * /data/data/com.termux/files/usr/bin/agy-backup backup --target all > /dev/null 2>&1
   ```
4. **Start Cron Service**:
   ```bash
   crond
   ```

---

### Method B: Android Native Job Scheduler (`termux-job-scheduler`)

Termux can schedule background Android system jobs that survive reboots:

```bash
termux-job-scheduler \
  --job-id 101 \
  --script "$PREFIX/bin/agy-backup backup --target all" \
  --period-ms 86400000 \
  --charging true \
  --net-connected true
```
*This schedules `agy-backup backup --target all` to run once every 24 hours (86,400,000 ms) while the phone is connected to Wi-Fi and charging.*

---

### Method C: AGY CLI `/schedule` Slash Command

Inside AGY CLI, you can schedule recurring automated backups using `/schedule`:

```
/schedule
Cron: "0 2 * * *"
Prompt: "Run `agy-backup backup --target all` to sync AGY user data to Google Drive."
```

---

## 📖 Complete Command Reference

| Command | Action |
|---|---|
| `agy-backup auth` | Authenticate with Google Drive OAuth2 |
| `agy-backup backup [-t target]` | Incremental cloud sync (`agy`, `gemini`, `termux`, `all`) |
| `agy-backup backup -l <dir_path>` | Save backup archive copy to local folder option |
| `agy-backup backup --local-only -l <path>` | Local-only backup (skip cloud upload) |
| `agy-backup backup --force` | Force backup creation even if no files changed |
| `agy-backup list` | List remote backup instances on Google Drive |
| `agy-backup restore [-t target] [id]` | Restore target user data from Google Drive |
| `agy-backup restore --local-file <path>` | Restore target user data from local file |
| `agy-backup rollback` | Emergency rollback to pre-restore local safety snapshot |
| `agy-backup status` | Show target paths, credentials, and snapshot status |

---

## 📄 License
Released under the [MIT License](LICENSE).
