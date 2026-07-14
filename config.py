"""
Web3 Job Bot Configuration
Everything sensitive or personal (email address, passwords, tokens) is read
from environment variables. When run via GitHub Actions, these come from
GitHub Secrets. NEVER hardcode passwords, tokens, or personal info in this file.
"""

import os

# User Profile
USER_PROFILE = {
    "name": "Muhammad Dawam",
    "skills": [
        "Web3 Marketing",
        "Solana Development",
        "Rust",
        "Anchor",
        "Customer Service",
        "UI/UX Design",
        "Coding",
        "Blockchain",
        "Crypto"
    ],
    "experience_level": "Junior-Mid",
    "preferred_location": ["Remote", "Europe"],
    "linkedin": "https://www.linkedin.com/in/muh-dawam",
    "github": "https://github.com/muhdawam94"
}

# Job Search Criteria
JOB_KEYWORDS = {
    "must_have": [
        "marketing", "growth", "community", "social media", "content",
        "developer", "engineer", "solana", "rust", "blockchain", "web3",
        "ui", "ux", "design", "frontend",
        "customer", "support", "success", "community manager"
    ],
    "nice_to_have": [
        "entry level", "junior", "mid-level", "remote", "europe",
        "anchor", "defi", "nft", "crypto"
    ],
    "exclude": [
        "senior 5+", "10+ years", "phd required", "lead", "principal",
        "onsite only", "us only", "visa required"
    ]
}

# Notification Settings
_email_address = os.environ.get("EMAIL_ADDRESS", "")

NOTIFICATIONS = {
    "email": {
        "enabled": bool(_email_address),
        "to": _email_address,
        "from": _email_address,
        "smtp_password": os.environ.get("GMAIL_APP_PASSWORD", "")
    },
    "telegram": {
        "enabled": bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
        "chat_id": os.environ.get("TELEGRAM_CHAT_ID", ""),
        "bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", "")
    },
    "discord": {
        "enabled": bool(os.environ.get("DISCORD_WEBHOOK_URL")),
        "webhook_url": os.environ.get("DISCORD_WEBHOOK_URL", "")
    }
}

# Bot Settings
BOT_CONFIG = {
    "check_interval_hours": 6,
    "max_jobs_per_notification": 10,
    "seen_jobs_file": "seen_jobs.json",
    "base_url": "https://web3.career"
}
