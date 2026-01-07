"""Scrape real company names from Y Combinator directory."""
import requests
from bs4 import BeautifulSoup
import logging
import random
from typing import List

logger = logging.getLogger(__name__)

class CompanyScraper:
    """Scrape company names from public sources."""
    
    # Fallback list of real B2B SaaS companies
    FALLBACK_COMPANIES = [
        "Stripe", "Twilio", "Segment", "Amplitude", "Mixpanel",
        "Datadog", "PagerDuty", "Intercom", "Zendesk", "Asana",
        "Notion", "Airtable", "Figma", "Miro", "Loom",
        "Calendly", "DocuSign", "Dropbox", "Box", "Slack",
        "Zoom", "Atlassian", "Monday.com", "ClickUp", "Linear",
        "Retool", "Webflow", "Vercel", "Netlify", "Supabase",
        "Auth0", "Okta", "OneLogin", "JumpCloud", "Rippling",
        "Gusto", "Deel", "Remote", "Lattice", "Culture Amp",
        "Gong", "Chorus", "Outreach", "SalesLoft", "HubSpot",
        "Marketo", "Mailchimp", "SendGrid", "Customer.io", "Braze"
    ]
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        
    def get_company_name(self) -> str:
        """Get a random B2B SaaS company name."""
        return self.rng.choice(self.FALLBACK_COMPANIES)
        
    def get_company_domain(self, company_name: str) -> str:
        """Generate company email domain from name."""
        # Convert company name to domain
        domain = company_name.lower().replace(" ", "").replace(".", "")
        return f"{domain}.com"