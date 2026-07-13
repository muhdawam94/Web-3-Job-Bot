"""
Main Web3 Job Bot
Orchestrates scraping, filtering, cover letter generation, and notifications
"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Set

from scraper import Web3CareerScraper
from filter import JobFilter
from cover_letter import CoverLetterGenerator
from notifier import Notifier
from config import USER_PROFILE, JOB_KEYWORDS, NOTIFICATIONS, BOT_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Web3JobBot:
    """Main bot orchestrator"""

    def __init__(self):
        self.config = {
            'USER_PROFILE': USER_PROFILE,
            'JOB_KEYWORDS': JOB_KEYWORDS,
            'NOTIFICATIONS': NOTIFICATIONS,
            'BOT_CONFIG': BOT_CONFIG
        }

        self.scraper = Web3CareerScraper()
        self.filter = JobFilter(self.config)
        self.cover_letter_gen = CoverLetterGenerator(USER_PROFILE)
        self.notifier = Notifier(self.config)

        self.seen_jobs_file = Path(BOT_CONFIG['seen_jobs_file'])
        self.seen_jobs = self._load_seen_jobs()

    def run(self):
        """Main bot execution"""
        logger.info("🤖 Web3 Job Bot Starting...")
        logger.info(f"👤 Profile: {USER_PROFILE['name']}")
        logger.info(f"🎯 Skills: {', '.join(USER_PROFILE['skills'][:5])}")
        logger.info(f"📍 Location: {', '.join(USER_PROFILE['preferred_location'])}")

        try:
            # Step 1: Scrape jobs
            logger.info("\n📡 Step 1: Scraping web3.career...")
            all_jobs = self.scraper.scrape_jobs(max_pages=3)
            logger.info(f"   Found {len(all_jobs)} total jobs")

            if not all_jobs:
                logger.warning("⚠️  No jobs found. Website might have changed structure.")
                return

            # Step 2: Filter for new jobs only
            logger.info("\n🔍 Step 2: Filtering for new jobs...")
            new_jobs = self._filter_new_jobs(all_jobs)
            logger.info(f"   {len(new_jobs)} new jobs (not seen before)")

            if not new_jobs:
                logger.info("✅ No new jobs since last check")
                return

            # Step 3: Filter by criteria
            logger.info("\n✨ Step 3: Matching jobs to your profile...")
            matching_jobs = self.filter.filter_jobs(new_jobs)
            logger.info(f"   {len(matching_jobs)} jobs match your criteria")

            if not matching_jobs:
                logger.info("📭 No matching jobs found")
                # Still mark them as seen
                self._mark_jobs_as_seen(new_jobs)
                return

            # Step 4: Generate cover letters
            logger.info("\n📝 Step 4: Generating cover letters...")
            cover_letters = {}
            for job in matching_jobs:
                job_id = job.get('id', 'unknown')
                try:
                    cover_letter = self.cover_letter_gen.generate(job)
                    cover_letters[job_id] = cover_letter
                    logger.info(f"   ✅ Generated for: {job.get('title', 'N/A')}")
                except Exception as e:
                    logger.error(f"   ❌ Failed for {job.get('title', 'N/A')}: {e}")

            # Step 5: Send notifications
            logger.info("\n📬 Step 5: Sending notifications...")

            # Limit to top N jobs to avoid spam
            max_jobs = BOT_CONFIG.get('max_jobs_per_notification', 10)
            jobs_to_notify = matching_jobs[:max_jobs]

            if len(matching_jobs) > max_jobs:
                logger.info(f"   Limiting to top {max_jobs} jobs (found {len(matching_jobs)})")

            self.notifier.send_all(jobs_to_notify, cover_letters)

            # Step 6: Mark as seen
            logger.info("\n💾 Step 6: Updating seen jobs...")
            self._mark_jobs_as_seen(new_jobs)

            # Summary
            logger.info("\n" + "=" * 80)
            logger.info("✅ BOT RUN COMPLETED")
            logger.info(f"   📊 Total scraped: {len(all_jobs)}")
            logger.info(f"   🆕 New jobs: {len(new_jobs)}")
            logger.info(f"   ✨ Matching: {len(matching_jobs)}")
            logger.info(f"   📬 Notified: {len(jobs_to_notify)}")
            logger.info("=" * 80)

            # Show top matches
            if matching_jobs:
                logger.info("\n🏆 TOP MATCHES:")
                for i, job in enumerate(matching_jobs[:5], 1):
                    logger.info(f"   {i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                    logger.info(f"      Score: {job.get('match_score', 0)} | {job.get('link', 'N/A')}")

        except Exception as e:
            logger.error(f"❌ Bot run failed: {e}", exc_info=True)

    def _filter_new_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter out jobs we've already seen"""
        new_jobs = []

        for job in jobs:
            job_id = job.get('id')
            if job_id and job_id not in self.seen_jobs:
                new_jobs.append(job)

        return new_jobs

    def _mark_jobs_as_seen(self, jobs: List[Dict]):
        """Mark jobs as seen and save to file"""
        for job in jobs:
            job_id = job.get('id')
            if job_id:
                self.seen_jobs.add(job_id)

        self._save_seen_jobs()
        logger.info(f"   Marked {len(jobs)} jobs as seen")

    def _load_seen_jobs(self) -> Set[str]:
        """Load seen jobs from file"""
        if self.seen_jobs_file.exists():
            try:
                with open(self.seen_jobs_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('seen_jobs', []))
            except Exception as e:
                logger.error(f"Error loading seen jobs: {e}")
                return set()
        return set()

    def _save_seen_jobs(self):
        """Save seen jobs to file"""
        try:
            data = {
                'seen_jobs': list(self.seen_jobs),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self.seen_jobs_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving seen jobs: {e}")


def main():
    """Entry point"""
    bot = Web3JobBot()
    bot.run()


if __name__ == "__main__":
    main()
