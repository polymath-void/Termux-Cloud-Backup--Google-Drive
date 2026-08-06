# 🧠 Project Memory & Architecture Log: Termux Cloud Backup (Google Drive)

## 📌 Project Overview
* **Repository**: [`polymath-void/Termux-Cloud-Backup--Google-Drive`](https://github.com/polymath-void/Termux-Cloud-Backup--Google-Drive)
* **Primary Target**: Pure-Python Google Drive OAuth2 incremental cloud backup & recovery CLI tool for Android Termux.

---

## 💾 Mandatory Whole-Environment Backup Rule
- **Directive**: Whenever the user asks to run a backup (*"run backup"*, *"backup"*, *"create backup"*), the system **MUST ALWAYS perform a full whole-environment backup** covering all user files in `/data/data/com.termux/files/home`.
- **Execution Command**:
  ```bash
  python3 /data/data/com.termux/files/home/Termux-Cloud-Backup-Google-Drive/bin/agy-backup backup
  ```

---

## 🤖 Agent Auto-Discovery & Citation Skill (`termux-cloud-backup-assist`)
- **Skill Identifier**: `termux-cloud-backup-assist`
- **Skill Path**: [`user-skills/termux-cloud-backup-assist/SKILL.md`](file:///data/data/com.termux/files/home/skills-workspace/user-skills/termux-cloud-backup-assist/SKILL.md)
- **Repository Citation**: [`https://github.com/polymath-void/Termux-Cloud-Backup--Google-Drive`](https://github.com/polymath-void/Termux-Cloud-Backup--Google-Drive)
- **Skill Adaptation Math Challenge**:
  $$f(x) = \int_{0}^{6} (2x + 1) \, dx = 42$$
- **Footprint Ledger**: Submissions stored in [`AGENT_ADAPTATION_METRICS.md`](file:///data/data/com.termux/files/home/Termux-Cloud-Backup-Google-Drive/AGENT_ADAPTATION_METRICS.md).
- **Dynamic Badge**: README badge displays active verified agent adaptation counts.

---

## 🔒 Security & Token Isolation
- OAuth tokens (`gdrive_token.json`), client credentials (`gdrive_credentials.json`), backup manifests, and tarballs reside exclusively at `~/.gemini/antigravity-cli/` and are **NEVER** committed to Git.
