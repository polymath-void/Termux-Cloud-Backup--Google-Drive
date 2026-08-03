# Termux Cloud Backup for Google Drive (`agy-backup`)

[![Platform](https://img.shields.io/badge/Platform-Android%20Termux-brightgreen)](https://termux.dev)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Storage](https://img.shields.io/badge/Cloud-Google%20Drive%20v3-orange)](https://developers.google.com/drive)

A lightweight, high-performance, pure-Python cloud backup & restoration tool engineered specifically for **Android Termux**. It provides **incremental update sync**, **manual local directory options**, and automated **Google Drive OAuth2 authentication** to back up and restore your **AGY CLI**, **Gemini CLI**, and **Termux user environment** databases.

---

## 🌟 Key Features

- 🔄 **Incremental Update Sync**: Uses SHA256 file manifest tracking to detect file changes. If no files changed, it skips redundant uploads. If files changed, it updates the existing cloud file instance rather than creating duplicate files.
- 📁 **Manual Local Directory Options**: Allows exporting/syncing backup archives to local folders (e.g., SD card, shared storage, or custom local directories).
- 🔑 **Headless Google Drive OAuth2**: Native OAuth2 Device Authorization Flow (`RFC 8628`), perfectly suited for terminal environments without desktop browser requirements.
- 🎯 **Multi-Target Backup Selector**:
  - `agy`: AGY CLI database (`~/.gemini/antigravity-cli`: settings, knowledge, skills, memory, conversations, brain, MCP)
  - `gemini`: Gemini CLI databases (`~/.gemini`: credentials, history, policies, state, project configs)
  - `termux`: Termux user environment (`~`: `.termux`, `.bashrc`, `.zshrc`, `.profile`, `.ssh`, `AGY`, `skills-workspace`)
  - `all`: All component targets combined.
- 🛡️ **Safety-First Restoration**: Automatically creates a local pre-restore snapshot (`~/.gemini/antigravity-cli.pre-restore.bak`) and verifies SHA256 checksums before extracting archives.

---

## 🚀 Use Cases

### 1. Daily Development Sync
Run `agy-backup backup --target all` at the end of your coding session. Only updated files, updated chat history, or new skills will be packed and synced to Google Drive `/AGY_Backups`.

### 2. Device Migration & Recovery
Moving to a new Android phone or setting up a fresh Termux installation? Install `agy-backup`, authenticate with Google Drive, and run `agy-backup restore` to instantly restore your entire AI development state, saved skills, and configurations.

### 3. Local SD Card Backup
Need an offline backup copy on local phone storage or an SD card without uploading to the cloud? Run `agy-backup backup -l ~/storage/downloads/Backups --local-only`.

### 4. Emergency State Rollback
If a restored backup or accidental configuration edit breaks your setup, run `agy-backup rollback` to instantly restore the pre-operation local snapshot.

---

## 🛠️ Installation & Setup

### 1. Clone & Initialize Local Repository
```bash
git clone ~/Termux-Cloud-Backup-Google-Drive
cd Termux-Cloud-Backup-Google-Drive
chmod +x bin/agy-backup
```

### 2. Link Executable to Path
```bash
ln -sf ~/Termux-Cloud-Backup-Google-Drive/bin/agy-backup $PREFIX/bin/agy-backup
termux-fix-shebang $PREFIX/bin/agy-backup
```

### 3. Verify Installation
```bash
agy-backup status
```

---

## 🔑 Google Drive Authentication Guide

`agy-backup` connects securely to Google Drive via **Google Drive API v3**.

1. **Obtain Google OAuth Client Credentials**:
   - Go to [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials).
   - Click **+ Create Credentials** $\rightarrow$ **OAuth client ID**.
   - Application type: **TVs and Limited Input devices** (or **Desktop app**).
   - Name: `AGY Backup` $\rightarrow$ Click **Create**.
   - Copy your **Client ID** and **Client Secret**.

2. **Authenticate in Termux**:
   ```bash
   agy-backup auth
   ```
   - Input your Client ID and Client Secret when prompted.
   - Open [https://www.google.com/device](https://www.google.com/device) and enter the 8-digit device code.
   - Once approved, access and refresh tokens will be saved to `~/.gemini/antigravity-cli/gdrive_token.json`.

---

## 📖 User Guide & Command Reference

### `agy-backup backup`
Perform incremental update sync for specified target components.

```bash
# Sync all targets (AGY, Gemini CLI, Termux) to Google Drive
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

### `agy-backup list`
List all remote backup instances stored in Google Drive `/AGY_Backups`.

```bash
agy-backup list
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
View target paths, credentials status, token validity, and local snapshot state.

```bash
agy-backup status
```

---

## 🔄 Incremental Update Mechanism

```
[ Local Files ] ---> [ SHA256 Hash Matrix ] vs [ Saved Manifest (backup_manifest.json) ]
                             |
              +--------------+--------------+
              |                             |
      (No Hashes Changed)           (Hashes Changed)
              |                             |
      [ Skip Upload ]            [ Generate Target .tar.gz ]
    "Up to date" printed                 |
                                 [ Update Remote File ID ]
                                 (Overwrites existing instance)
```

1. **Manifest File**: `~/.gemini/antigravity-cli/backup_manifest.json`
2. **File Checksum Comparison**: Scans included paths, computes SHA256 hashes, and compares against the previous run.
3. **Single Remote Instance**: Overwrites/updates the existing remote file ID on Google Drive (e.g. `agy_backup_latest.tar.gz`) instead of cluttering your cloud storage with thousands of duplicate files.

---

## 📄 License
Released under the [MIT License](LICENSE).
