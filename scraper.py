"""
Web3.careers job scraper
Scrapes job listings from web3.career
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Web3CareerScraper:
    """Scraper for web3.career job listings"""

    def __init__(self, base_url: str = "https://web3.career"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_jobs(self, max_pages: int = 3) -> List[Dict]:
        """
        Scrape job listings from web3.career

        Args:
            max_pages: Number of pages to scrape (default 3 = ~60 jobs)

        Returns:
            List of job dictionaries
        """
        jobs = []

        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}/{max_pages}...")

            try:
                # Web3.career uses simple pagination
                url = f"{self.base_url}" if page == 1 else f"{self.base_url}?page={page}"

                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find job listings - adjust selectors based on actual site structure
                job_cards = soup.find_all('tr', class_='table_row')

                if not job_cards:
                    # Try alternative selector
                    job_cards = soup.find_all('div', class_='job-card')

                logger.info(f"Found {len(job_cards)} jobs on page {page}")

                for card in job_cards:
                    try:
                        job = self._parse_job_card(card)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        logger.error(f"Error parsing job card: {e}")
                        continue

                # Be respectful - don't hammer the server
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                continue

        logger.info(f"Total jobs scraped: {len(jobs)}")
        return jobs

    def _parse_job_card(self, card) -> Dict:
        """
        Parse individual job card into structured data

        Returns:
            Dict with job details
        """
        job = {}

        try:
            # Try to extract job title
            title_elem = card.find('h2') or card.find('h3') or card.find('a', class_='job-title')
            if title_elem:
                job['title'] = title_elem.get_text(strip=True)

                # Get job link
                link = title_elem.find('a') or card.find('a')
                if link and link.get('href'):
                    href = link['href']
                    job['link'] = href if href.startswith('http') else f"{self.base_url}{href}"
                    # Extract job ID from URL
                    job['id'] = href.split('/')[-1] if '/' in href else href

            # Extract company
            company_elem = card.find('span', class_='company-name') or card.find('td', class_='company-logo')
            if company_elem:
                job['company'] = company_elem.get_text(strip=True)

            # Extract location
            location_elem = card.find('span', class_='location') or card.find('td', class_='location')
            if location_elem:
                job['location'] = location_elem.get_text(strip=True)

            # Extract salary if available
            salary_elem = card.find('span', class_='salary') or card.find('td', class_='salary')
            if salary_elem:
                job['salary'] = salary_elem.get_text(strip=True)

            # Extract tags/categories
            tags = []
            tag_elems = card.find_all('span', class_='tag') or card.find_all('a', class_='badge')
            for tag in tag_elems:
                tags.append(tag.get_text(strip=True))
            job['tags'] = tags

            # Try to get job description (might need separate request)
            desc_elem = card.find('p', class_='description') or card.find('div', class_='job-description')
            if desc_elem:
                job['description'] = desc_elem.get_text(strip=True)[:500]  # First 500 chars

            # Add timestamp
            job['scraped_at'] = time.strftime('%Y-%m-%d %H:%M:%S')

            # Only return if we have at least title and link
            if 'title' in job and 'link' in job:
                return job

        except Exception as e:
            logger.error(f"Error parsing job details: {e}")

        return None

    def get_job_details(self, job_url: str) -> Dict:
        """
        Get full job details from individual job page
        Used to get complete description for cover letter
        """
        try:
            response = requests.get(job_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            details = {}

            # Extract full description
            desc_elem = soup.find('div', class_='job-description') or soup.find('div', class_='description')
            if desc_elem:
                details['full_description'] = desc_elem.get_text(strip=True)

            # Extract requirements
            req_elem = soup.find('div', class_='requirements') or soup.find('ul', class_='requirements')
            if req_elem:
                details['requirements'] = req_elem.get_text(strip=True)

            # Extract benefits
            benefits_elem = soup.find('div', class_='benefits')
            if benefits_elem:
                details['benefits'] = benefits_elem.get_text(strip=True)

            return details

        except Exception as e:
            logger.error(f"Error getting job details from {job_url}: {e}")
            return {}


if __name__ == "__main__":
    # Test scraper
    scraper = Web3CareerScraper()
    jobs = scraper.scrape_jobs(max_pages=1)

    print(f"\n=== Found {len(jobs)} jobs ===\n")
    for job in jobs[:3]:  # Show first 3
        print(f"Title: {job.get('title', 'N/A')}")
        print(f"Company: {job.get('company', 'N/A')}")
        print(f"Location: {job.get('location', 'N/A')}")
        print(f"Link: {job.get('link', 'N/A')}")
        print(f"Tags: {', '.join(job.get('tags', []))}")
        print("-" * 80)
