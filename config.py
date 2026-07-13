"""
Web3 Job Bot Configuration
Credentials are read from environment variables (GitHub Secrets when run via
GitHub Actions, or a local .env / OS environment variable when run locally).
NEVER hardcode passwords or tokens directly in this file.
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
        # Marketing related
        "marketing", "growth", "community", "social media", "content",
        # Development related
        "developer", "engineer", "solana", "rust", "blockchain", "web3",
        # Design/UX related
        "ui", "ux", "design", "frontend",
        # Customer facing
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
NOTIFICATIONS = {
    "email": {
        "enabled": True,
        "to": "muhdawam94@gmail.com",
        "from": "muhdawam94@gmail.com",
        # Gmail App Password required (not regular password)
        # Get it from: https://myaccount.google.com/apppasswords
        # Set as GitHub Secret: GMAIL_APP_PASSWORD
        "smtp_password": os.environ.get("GMAIL_APP_PASSWORD", "")
    },
    "telegram": {
        # Auto-enabled if a bot token is provided via secrets
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
    "max_jobs_per_notification": 10,  # Avoid spam if too many jobs found
    "seen_jobs_file": "seen_jobs.json",
    "base_url": "https://web3.career"
}
