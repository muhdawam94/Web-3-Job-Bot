"""
Cover letter generator
Generates tailored cover letters for each job
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """Generate professional cover letters"""

    def __init__(self, user_profile: Dict):
        self.profile = user_profile

    def generate(self, job: Dict) -> str:
        """
        Generate cover letter for a specific job

        Args:
            job: Job dictionary with title, company, description, etc.

        Returns:
            Formatted cover letter string
        """
        # Determine job category for targeted intro
        job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()

        # Categorize job
        category = self._categorize_job(job_text)

        # Generate appropriate intro paragraph
        intro = self._generate_intro(category, job)

        # Generate skills paragraph
        skills_para = self._generate_skills_paragraph(category, job)

        # Generate closing
        closing = self._generate_closing()

        # Assemble cover letter
        cover_letter = f"""Dear Hiring Manager at {job.get('company', 'your company')},

{intro}

{skills_para}

I'm particularly drawn to {job.get('company', 'your company')} because of your work in the Web3 space. As someone who's passionate about blockchain technology and its potential to reshape industries, I'm excited about the opportunity to contribute to your mission.

{closing}

Best regards,
{self.profile.get('name', 'Muhammad Dawam')}

LinkedIn: {self.profile.get('linkedin', 'https://www.linkedin.com/in/muh-dawam')}
GitHub: {self.profile.get('github', 'https://github.com/muhdawam94')}
"""

        return cover_letter

    def _categorize_job(self, job_text: str) -> str:
        """Categorize job into main type"""

        if any(kw in job_text for kw in ['developer', 'engineer', 'solana', 'rust', 'coding']):
            return 'development'
        elif any(kw in job_text for kw in ['marketing', 'growth', 'community', 'social']):
            return 'marketing'
        elif any(kw in job_text for kw in ['design', 'ui', 'ux', 'frontend']):
            return 'design'
        elif any(kw in job_text for kw in ['customer', 'support', 'success']):
            return 'support'
        else:
            return 'general'

    def _generate_intro(self, category: str, job: Dict) -> str:
        """Generate intro paragraph based on job category"""

        title = job.get('title', 'this position')

        intros = {
            'development': f"I'm writing to express my strong interest in the {title} position. As a Solana developer with hands-on experience in Rust and Anchor framework, I'm excited about the opportunity to contribute to your blockchain development team.",

            'marketing': f"I'm excited to apply for the {title} role. With my background in Web3 marketing and deep understanding of blockchain technology, I bring a unique combination of technical knowledge and marketing expertise that allows me to craft compelling narratives for crypto products.",

            'design': f"I'm writing to apply for the {title} position. As a UI/UX designer with a focus on Web3 applications, I understand the unique challenges of creating intuitive experiences for blockchain products while maintaining the security and transparency that users expect.",

            'support': f"I'm interested in the {title} role at your company. My experience in customer service combined with my technical knowledge of Web3 technologies allows me to provide exceptional support while helping users navigate the complexities of blockchain applications.",

            'general': f"I'm writing to express my interest in the {title} position. With my diverse background spanning Web3 development, marketing, and user experience, I bring a well-rounded skill set that allows me to contribute across multiple dimensions of your product and team."
        }

        return intros.get(category, intros['general'])

    def _generate_skills_paragraph(self, category: str, job: Dict) -> str:
        """Generate skills paragraph based on job category"""

        skills_paras = {
            'development': "My technical expertise includes Solana smart contract development using Rust and the Anchor framework, with a strong focus on code optimization and security best practices. I've worked on optimizing compute units, managing account structures, and implementing efficient on-chain programs. Beyond coding, I understand the importance of clear technical communication and can bridge the gap between technical implementation and user-facing features.",

            'marketing': "I've developed comprehensive go-to-market strategies for Web3 projects, combining deep technical understanding with marketing best practices. My unique advantage is that I can read smart contract code, understand protocol mechanics, and translate complex blockchain concepts into compelling marketing messages. This technical foundation allows me to create authentic, technically-accurate content that resonates with the crypto-native audience.",

            'design': "My design approach combines aesthetic appeal with functionality, always keeping the end-user experience at the forefront. I'm experienced in creating intuitive interfaces for complex blockchain interactions, making Web3 applications accessible to both crypto-natives and newcomers. I understand the importance of clear visual hierarchies, responsive design, and the unique UX considerations of decentralized applications.",

            'support': "I excel at breaking down complex technical concepts into clear, actionable guidance that users can follow. My technical background in blockchain development allows me to troubleshoot issues effectively and provide accurate solutions. I'm patient, empathetic, and committed to ensuring every user interaction is positive and productive, whether I'm helping a beginner set up their first wallet or assisting a power user with advanced features.",

            'general': "My diverse skill set spans multiple areas: I can write and optimize Solana smart contracts, design intuitive user interfaces, craft compelling marketing narratives, and provide excellent customer support. This versatility allows me to contribute wherever the team needs support and to understand how different parts of the product ecosystem fit together. I'm a quick learner who thrives in fast-paced startup environments."
        }

        return skills_paras.get(category, skills_paras['general'])

    def _generate_closing(self) -> str:
        """Generate closing paragraph"""

        return "I'd love the opportunity to discuss how my skills and passion for Web3 can contribute to your team's success. I'm available for a call at your convenience and can start immediately. Thank you for considering my application."

    def generate_quick_pitch(self, job: Dict) -> str:
        """
        Generate short pitch for notifications

        Args:
            job: Job dictionary

        Returns:
            Brief pitch (2-3 sentences)
        """
        category = self._categorize_job(f"{job.get('title', '')} {job.get('description', '')}".lower())

        pitches = {
            'development': f"Solana developer with Rust/Anchor experience. Strong focus on code optimization and smart contract security. Ready to contribute to your blockchain development team.",

            'marketing': f"Web3 marketer with technical blockchain knowledge. Can bridge the gap between complex protocol mechanics and compelling marketing narratives. Experienced in community growth and go-to-market strategy.",

            'design': f"UI/UX designer specialized in Web3 applications. Creating intuitive experiences for blockchain products. Strong understanding of user flows in decentralized applications.",

            'support': f"Customer support specialist with blockchain technical knowledge. Can troubleshoot complex issues and explain Web3 concepts clearly. Patient and user-focused.",

            'general': f"Versatile Web3 professional with skills in development, marketing, and design. Quick learner who thrives in startup environments. Ready to contribute across multiple areas."
        }

        return pitches.get(category, pitches['general'])


if __name__ == "__main__":
    # Test cover letter generator
    from config import USER_PROFILE

    test_job = {
        'title': 'Junior Solana Developer',
        'company': 'Web3 Startup',
        'description': 'Looking for a junior Solana developer with Rust experience to join our DeFi team.',
        'location': 'Remote - Europe'
    }

    generator = CoverLetterGenerator(USER_PROFILE)
    cover_letter = generator.generate(test_job)

    print("\n=== Generated Cover Letter ===\n")
    print(cover_letter)
    print("\n=== Quick Pitch ===\n")
    print(generator.generate_quick_pitch(test_job))
