"""
Notification system
Sends job alerts via Email, Telegram, and Discord
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    """Send notifications via multiple channels"""

    def __init__(self, config: Dict):
        self.config = config
        self.email_config = config.get('NOTIFICATIONS', {}).get('email', {})
        self.telegram_config = config.get('NOTIFICATIONS', {}).get('telegram', {})
        self.discord_config = config.get('NOTIFICATIONS', {}).get('discord', {})

    def send_all(self, jobs: List[Dict], cover_letters: Dict[str, str]):
        """
        Send notifications via all enabled channels

        Args:
            jobs: List of matching jobs
            cover_letters: Dict mapping job IDs to cover letters
        """
        if not jobs:
            logger.info("No jobs to notify about")
            return

        logger.info(f"Sending notifications for {len(jobs)} jobs")

        # Send via each enabled channel
        if self.email_config.get('enabled'):
            self._send_email(jobs, cover_letters)

        if self.telegram_config.get('enabled'):
            self._send_telegram(jobs, cover_letters)

        if self.discord_config.get('enabled'):
            self._send_discord(jobs, cover_letters)

    def _send_email(self, jobs: List[Dict], cover_letters: Dict):
        """Send email notification"""
        try:
            # Build email content
            subject = f"🚀 {len(jobs)} New Web3 Jobs Found!"

            body = self._build_email_body(jobs, cover_letters)

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']

            # Attach HTML and plain text versions
            msg.attach(MIMEText(body, 'plain'))

            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(
                    self.email_config['from'],
                    self.email_config['smtp_password']
                )
                server.send_message(msg)

            logger.info(f"✅ Email sent to {self.email_config['to']}")

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")

    def _build_email_body(self, jobs: List[Dict], cover_letters: Dict) -> str:
        """Build formatted email body"""

        body = f"""🚀 {len(jobs)} NEW WEB3 JOBS FOUND!

Your Web3 job bot found {len(jobs)} matching positions. Here are the details:

{"=" * 80}

"""

        for i, job in enumerate(jobs, 1):
            job_id = job.get('id', 'unknown')
            cover_letter = cover_letters.get(job_id, 'No cover letter generated')

            body += f"""
JOB #{i}
{"-" * 80}
📋 Title: {job.get('title', 'N/A')}
🏢 Company: {job.get('company', 'N/A')}
📍 Location: {job.get('location', 'N/A')}
💰 Salary: {job.get('salary', 'Not specified')}
🏷️  Tags: {', '.join(job.get('tags', []))}
⭐ Match Score: {job.get('match_score', 0)}/100
💡 Why it matches: {', '.join(job.get('match_reasons', []))}

🔗 APPLY HERE: {job.get('link', 'N/A')}

📝 COVER LETTER (ready to copy-paste):
{"-" * 80}
{cover_letter}
{"-" * 80}

{"=" * 80}

"""

        body += f"""
⏱️  QUICK ACTIONS:
1. Click the job link above
2. Copy the cover letter
3. Paste and customize if needed
4. Submit application

💡 TIP: Apply within 24 hours for best response rates!

---
Sent by your Web3 Job Bot 🤖
"""

        return body

    def _send_telegram(self, jobs: List[Dict], cover_letters: Dict):
        """Send Telegram notification"""
        try:
            bot_token = self.telegram_config.get('bot_token')
            chat_id = self.telegram_config.get('chat_id')

            if not bot_token or not chat_id:
                logger.warning("⚠️  Telegram not configured (missing bot_token or chat_id)")
                return

            # Telegram API
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

            # Send summary message first
            summary = f"🚀 *{len(jobs)} New Web3 Jobs Found!*\n\n"

            for i, job in enumerate(jobs[:5], 1):  # First 5 jobs in summary
                summary += f"{i}. *{job.get('title', 'N/A')}* at {job.get('company', 'N/A')}\n"
                summary += f"   📍 {job.get('location', 'N/A')} | ⭐ Score: {job.get('match_score', 0)}\n"
                summary += f"   🔗 [Apply Here]({job.get('link', 'N/A')})\n\n"

            requests.post(url, json={
                'chat_id': chat_id,
                'text': summary,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            })

            # Send individual cover letters (as separate messages to avoid length limit)
            for job in jobs[:3]:  # Top 3 jobs get full cover letters
                job_id = job.get('id', 'unknown')
                cover_letter = cover_letters.get(job_id, '')

                if cover_letter:
                    msg = f"📝 *Cover Letter for: {job.get('title', 'N/A')}*\n\n{cover_letter[:4000]}"
                    requests.post(url, json={
                        'chat_id': chat_id,
                        'text': msg,
                        'parse_mode': 'Markdown'
                    })

            logger.info(f"✅ Telegram message sent to {chat_id}")

        except Exception as e:
            logger.error(f"❌ Failed to send Telegram: {e}")

    def _send_discord(self, jobs: List[Dict], cover_letters: Dict):
        """Send Discord webhook notification"""
        try:
            webhook_url = self.discord_config.get('webhook_url')

            if not webhook_url:
                logger.warning("⚠️  Discord not configured (missing webhook_url)")
                return

            # Build Discord embed
            embeds = []

            # Summary embed
            embeds.append({
                "title": f"🚀 {len(jobs)} New Web3 Jobs Found!",
                "description": f"Your job bot found {len(jobs)} matching positions",
                "color": 5814783,  # Blue color
                "fields": [
                    {
                        "name": "📊 Summary",
                        "value": f"Top matches ready to apply!",
                        "inline": False
                    }
                ]
            })

            # Job embeds (max 3)
            for job in jobs[:3]:
                job_embed = {
                    "title": f"📋 {job.get('title', 'N/A')}",
                    "description": f"**{job.get('company', 'N/A')}**",
                    "url": job.get('link', ''),
                    "color": 3066993,  # Green
                    "fields": [
                        {
                            "name": "📍 Location",
                            "value": job.get('location', 'N/A'),
                            "inline": True
                        },
                        {
                            "name": "⭐ Match Score",
                            "value": str(job.get('match_score', 0)),
                            "inline": True
                        },
                        {
                            "name": "🏷️ Tags",
                            "value": ', '.join(job.get('tags', [])[:3]) or 'None',
                            "inline": False
                        },
                        {
                            "name": "💡 Why it matches",
                            "value": ', '.join(job.get('match_reasons', [])[:2]) or 'Good fit',
                            "inline": False
                        }
                    ]
                }

                # Add salary if available
                if job.get('salary'):
                    job_embed['fields'].insert(2, {
                        "name": "💰 Salary",
                        "value": job.get('salary'),
                        "inline": True
                    })

                embeds.append(job_embed)

            # Send to Discord
            payload = {
                "embeds": embeds,
                "username": "Web3 Job Bot",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/3227/3227324.png"
            }

            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()

            logger.info("✅ Discord notification sent")

        except Exception as e:
            logger.error(f"❌ Failed to send Discord: {e}")


if __name__ == "__main__":
    # Test notifier
    from config import NOTIFICATIONS, USER_PROFILE

    test_jobs = [{
        'id': 'test-123',
        'title': 'Junior Solana Developer',
        'company': 'Web3 Startup',
        'location': 'Remote - Europe',
        'salary': '$60k-$80k',
        'tags': ['solana', 'rust', 'remote'],
        'link': 'https://web3.career/job/123',
        'match_score': 85,
        'match_reasons': ['Matches Solana/Rust', 'Remote position']
    }]

    test_cover_letters = {
        'test-123': "Dear Hiring Manager,\n\nI'm interested in the Junior Solana Developer position...\n\nBest regards,\nMuhammad Dawam"
    }

    config = {
        'NOTIFICATIONS': NOTIFICATIONS,
        'USER_PROFILE': USER_PROFILE
    }

    notifier = Notifier(config)

    print("Testing notifier (will fail if credentials not configured)...")
    print("Configure email/telegram/discord in config.py first")
    # notifier.send_all(test_jobs, test_cover_letters)
