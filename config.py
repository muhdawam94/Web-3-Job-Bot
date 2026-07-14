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
