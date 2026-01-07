"""Generate user data with realistic demographics."""

import logging
import random
import uuid
from typing import List
from datetime import timedelta

from src.models.schema import User
from src.scrapers.name_generator import NameGenerator
from src.utils.temporal import TemporalGenerator
from src.config import Config

logger = logging.getLogger(__name__)


class UserGenerator:
    """Generate user entities with realistic demographics."""

    JOB_TITLES = {
        "engineering": [
            "Software Engineer", "Senior Software Engineer", "Staff Engineer",
            "Engineering Manager", "Tech Lead", "Frontend Engineer",
            "Backend Engineer", "Full Stack Engineer", "DevOps Engineer",
            "QA Engineer", "Security Engineer", "Data Engineer",
        ],
        "product": [
            "Product Manager", "Senior Product Manager", "Product Lead",
            "Product Designer", "UX Researcher", "Product Analyst",
            "Technical Product Manager", "Group Product Manager",
        ],
        "marketing": [
            "Marketing Manager", "Content Marketing Manager", "Growth Manager",
            "Social Media Manager", "Brand Manager", "Marketing Analyst",
            "SEO Specialist", "Demand Generation Manager", "Product Marketing Manager",
        ],
        "sales": [
            "Account Executive", "Sales Development Rep", "Sales Manager",
            "Enterprise Account Executive", "Customer Success Manager",
            "Sales Engineer", "Business Development Rep", "VP of Sales",
        ],
        "operations": [
            "Operations Manager", "HR Manager", "Finance Manager",
            "Office Manager", "Recruiter", "Financial Analyst",
            "People Operations", "Chief of Staff", "Executive Assistant",
        ],
    }

    def __init__(self, organization_id: str, domain: str, seed: int = 42):
        self.organization_id = organization_id
        self.domain = domain

        self.name_gen = NameGenerator(seed=seed)
        self.temporal_gen = TemporalGenerator(
            Config.SIMULATION_START_DATE,
            Config.SIMULATION_END_DATE,
            seed=seed,
        )

        self.rng = random.Random(seed)

    def generate_users(self, count: int, department: str) -> List[User]:
        """Generate multiple users for a department."""
        users = []

        for _ in range(count):
            first_name, last_name = self.name_gen.generate_name()
            full_name = f"{first_name} {last_name}"

            # ---------- GUARANTEED UNIQUE EMAIL ----------
            base_email = self.name_gen.generate_email(
                first_name, last_name, self.domain
            )
            unique_suffix = uuid.uuid4().hex[:8]
            email = base_email.replace("@", f".{unique_suffix}@")
            # --------------------------------------------

            job_title = self.rng.choice(
                self.JOB_TITLES.get(department, ["Team Member"])
            )

            role = "admin" if self.rng.random() < 0.05 else "member"

            created_at = self.temporal_gen.random_date_in_range(
                Config.SIMULATION_START_DATE,
                Config.SIMULATION_END_DATE - timedelta(days=30),
            )

            is_active = self.rng.random() < 0.98

            user = User(
                organization_id=self.organization_id,
                email=email,
                name=full_name,
                role=role,
                job_title=job_title,
                department=department,
                created_at=created_at,
                is_active=is_active,
                photo_url=f"https://i.pravatar.cc/150?u={email}",
            )

            users.append(user)

        logger.info(f"Generated {count} users for {department} department")
        return users
