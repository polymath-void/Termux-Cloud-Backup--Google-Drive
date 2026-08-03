import os
from pathlib import Path

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))

# Targets configuration
TARGET_PATHS = {
    "agy": HOME / ".gemini" / "antigravity-cli",
    "gemini": HOME / ".gemini",
    "termux": HOME,
}

GDRIVE_FOLDER_NAME = "AGY_Backups"
MAX_BACKUPS = 10

CREDENTIALS_FILE = HOME / ".gemini" / "antigravity-cli" / "gdrive_credentials.json"
TOKEN_FILE = HOME / ".gemini" / "antigravity-cli" / "gdrive_token.json"
MANIFEST_FILE = HOME / ".gemini" / "antigravity-cli" / "backup_manifest.json"
TEMP_DIR = HOME / ".gemini" / "antigravity-cli" / "scratch" / "agy_backup_tmp"

# Inclusions per target
TARGET_INCLUSIONS = {
    "agy": [
        "settings.json",
        "knowledge",
        "skills",
        "memory",
        "history.jsonl",
        "conversations",
        "conversation_summaries.db",
        "brain",
        "mcp_config.json",
        "mcp",
    ],
    "gemini": [
        "GEMINI.md",
        "config",
        "gemini-credentials.json",
        "google_accounts.json",
        "history",
        "policies",
        "projects.json",
        "rules",
        "settings.json",
        "skills",
        "state.json",
        "trustedFolders.json",
    ],
    "termux": [
        ".termux",
        ".bashrc",
        ".zshrc",
        ".profile",
        ".gitconfig",
        ".ssh",
        "AGY",
        "skills-workspace",
    ]
}

# Universal exclusions
EXCLUDED_PATTERNS = [
    "cache",
    ".cache",
    "node_modules",
    "cli.log",
    "crashes",
    "updater",
    "*.lock",
    "*.tmp",
    "scratch/agy_backup_tmp",
    ".git/objects",
]
