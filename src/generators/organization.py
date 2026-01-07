"""Generate organization and workspace data."""
import logging
from datetime import datetime
from src.models.schema import Organization
from src.scrapers.company_scraper import CompanyScraper
from src.config import Config

logger = logging.getLogger(__name__)

class OrganizationGenerator:
    """Generate organization/workspace entities."""
    
    def __init__(self, seed: int = 42):
        self.scraper = CompanyScraper(seed=seed)
        
    def generate(self) -> Organization:
        """Generate a single organization."""
        company_name = self.scraper.get_company_name()
        domain = self.scraper.get_company_domain(company_name)
        
        org = Organization(
            name=company_name,
            domain=domain,
            created_at=Config.SIMULATION_START_DATE,
            is_organization=True,
            settings={
                "default_view": "list",
                "color_coding_enabled": True,
                "time_tracking_enabled": True
            }
        )
        
        logger.info(f"Generated organization: {org.name}")
        return org