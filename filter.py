"""
Job filtering logic
Filters scraped jobs based on user criteria and keywords
"""

import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobFilter:
    """Filter jobs based on keywords and criteria"""

    def __init__(self, config: Dict):
        self.keywords = config.get('JOB_KEYWORDS', {})
        self.user_profile = config.get('USER_PROFILE', {})

        self.must_have = [kw.lower() for kw in self.keywords.get('must_have', [])]
        self.nice_to_have = [kw.lower() for kw in self.keywords.get('nice_to_have', [])]
        self.exclude = [kw.lower() for kw in self.keywords.get('exclude', [])]

    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Filter jobs based on criteria

        Args:
            jobs: List of scraped job dictionaries

        Returns:
            List of filtered jobs with match scores
        """
        filtered = []

        for job in jobs:
            match_score = self._calculate_match_score(job)

            if match_score['total_score'] > 0:
                job['match_score'] = match_score['total_score']
                job['match_reasons'] = match_score['reasons']
                filtered.append(job)

        # Sort by match score (highest first)
        filtered.sort(key=lambda x: x['match_score'], reverse=True)

        logger.info(f"Filtered {len(filtered)}/{len(jobs)} jobs")
        return filtered

    def _calculate_match_score(self, job: Dict) -> Dict:
        """
        Calculate how well a job matches user criteria

        Returns:
            Dict with total_score and reasons
        """
        score = 0
        reasons = []

        # Combine all job text for searching
        job_text = ' '.join([
            job.get('title', ''),
            job.get('description', ''),
            job.get('company', ''),
            job.get('location', ''),
            ' '.join(job.get('tags', []))
        ]).lower()

        # Check for exclude keywords first (immediate disqualification)
        for keyword in self.exclude:
            if keyword in job_text:
                logger.debug(f"Job excluded due to keyword: {keyword}")
                return {'total_score': 0, 'reasons': [f"Contains excluded term: {keyword}"]}

        # Check must_have keywords (high score)
        must_have_matches = []
        for keyword in self.must_have:
            if keyword in job_text:
                score += 10
                must_have_matches.append(keyword)

        if must_have_matches:
            reasons.append(f"Matches key skills: {', '.join(must_have_matches[:3])}")

        # Check nice_to_have keywords (medium score)
        nice_to_have_matches = []
        for keyword in self.nice_to_have:
            if keyword in job_text:
                score += 3
                nice_to_have_matches.append(keyword)

        if nice_to_have_matches:
            reasons.append(f"Also matches: {', '.join(nice_to_have_matches[:3])}")

        # Bonus for remote
        if 'remote' in job_text:
            score += 5
            reasons.append("Remote position")

        # Bonus for Europe
        europe_keywords = ['europe', 'eu', 'european', 'berlin', 'london', 'amsterdam', 'paris']
        for keyword in europe_keywords:
            if keyword in job_text:
                score += 5
                reasons.append("Europe-friendly")
                break

        # Bonus for entry/junior level
        entry_keywords = ['entry', 'junior', 'mid-level', '1-3 years', '2-4 years']
        for keyword in entry_keywords:
            if keyword in job_text:
                score += 5
                reasons.append("Appropriate seniority level")
                break

        # Penalty for senior-only positions (but don't exclude completely)
        senior_keywords = ['senior 5+', '7+ years', '10+ years', 'staff engineer', 'principal']
        for keyword in senior_keywords:
            if keyword in job_text:
                score -= 10
                reasons.append("May require more experience")
                break

        return {
            'total_score': max(0, score),  # Don't go negative
            'reasons': reasons
        }

    def is_match(self, job: Dict, min_score: int = 10) -> bool:
        """
        Quick check if job matches criteria

        Args:
            job: Job dictionary
            min_score: Minimum score to be considered a match

        Returns:
            True if job matches, False otherwise
        """
        match_score = self._calculate_match_score(job)
        return match_score['total_score'] >= min_score


if __name__ == "__main__":
    # Test filter
    from config import JOB_KEYWORDS, USER_PROFILE

    test_jobs = [
        {
            'title': 'Junior Solana Developer',
            'company': 'Web3 Startup',
            'description': 'Looking for a junior Solana developer with Rust experience',
            'location': 'Remote - Europe',
            'tags': ['solana', 'rust', 'remote']
        },
        {
            'title': 'Senior Backend Engineer (10+ years)',
            'company': 'TradFi Corp',
            'description': 'Need experienced backend engineer',
            'location': 'San Francisco - Onsite',
            'tags': ['backend', 'senior']
        },
        {
            'title': 'Web3 Marketing Manager',
            'company': 'DeFi Protocol',
            'description': 'Community growth and marketing for DeFi protocol',
            'location': 'Remote',
            'tags': ['marketing', 'web3', 'remote']
        }
    ]

    filter = JobFilter({'JOB_KEYWORDS': JOB_KEYWORDS, 'USER_PROFILE': USER_PROFILE})
    filtered = filter.filter_jobs(test_jobs)

    print(f"\n=== Filtered {len(filtered)} / {len(test_jobs)} jobs ===\n")
    for job in filtered:
        print(f"Title: {job['title']}")
        print(f"Score: {job['match_score']}")
        print(f"Reasons: {', '.join(job['match_reasons'])}")
        print("-" * 80)
