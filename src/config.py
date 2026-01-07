"""Configuration management for Asana simulation."""
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration for the simulation."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Simulation Parameters
    COMPANY_SIZE = int(os.getenv('COMPANY_SIZE', 7500))
    RANDOM_SEED = int(os.getenv('RANDOM_SEED', 42))
    
    # Date ranges
    SIMULATION_START_DATE = datetime.strptime(
        os.getenv('SIMULATION_START_DATE', '2023-07-01'),
        '%Y-%m-%d'
    )
    SIMULATION_END_DATE = datetime.now()
    
    # LLM Configuration
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.8))
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 500))
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'output/asana_simulation.sqlite')
    
    # Team Distribution (based on typical B2B SaaS company)
    TEAM_DISTRIBUTION = {
        'engineering': 0.35,  # 35% engineers
        'product': 0.10,      # 10% product
        'marketing': 0.15,    # 15% marketing
        'sales': 0.25,        # 25% sales
        'operations': 0.15    # 15% operations (HR, Finance, etc.)
    }
    
    # Project Types Distribution
    PROJECT_TYPE_DISTRIBUTION = {
        'sprint': 0.30,
        'kanban': 0.25,
        'timeline': 0.20,
        'list': 0.20,
        'calendar': 0.05
    }
    
    # Task Completion Rates by Project Type
    # Source: Asana "Anatomy of Work Index 2023"
    COMPLETION_RATES = {
        'sprint': (0.70, 0.85),      # Sprint projects have higher completion
        'kanban': (0.60, 0.75),
        'timeline': (0.55, 0.70),
        'list': (0.50, 0.65),
        'calendar': (0.65, 0.80)
    }
    
    # Due Date Distribution
    # Source: Atlassian "State of Teams 2023"
    DUE_DATE_DISTRIBUTION = {
        'within_1_week': 0.25,
        'within_1_month': 0.40,
        'within_3_months': 0.20,
        'no_due_date': 0.10,
        'overdue': 0.05
    }
    
    # Task Assignment Rate
    # Source: Asana benchmarks - 15% of tasks typically unassigned
    TASK_ASSIGNMENT_RATE = 0.85
    
    # Asana Colors
    ASANA_COLORS = [
        'light-pink', 'light-green', 'light-blue', 'light-red', 'light-teal',
        'light-brown', 'light-orange', 'light-purple', 'light-warm-gray',
        'dark-pink', 'dark-green', 'dark-blue', 'dark-red', 'dark-teal',
        'dark-brown', 'dark-orange', 'dark-purple', 'dark-warm-gray'
    ]
    
    # Section Names by Project Type
    SECTION_TEMPLATES = {
        'sprint': ['Backlog', 'To Do', 'In Progress', 'In Review', 'Done'],
        'kanban': ['To Do', 'In Progress', 'Done'],
        'timeline': ['Planning', 'Execution', 'Review', 'Complete'],
        'list': ['Not Started', 'In Progress', 'Completed'],
        'calendar': ['Upcoming', 'This Week', 'This Month', 'Completed']
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        if cls.COMPANY_SIZE < 5000 or cls.COMPANY_SIZE > 10000:
            raise ValueError("COMPANY_SIZE must be between 5000 and 10000")
        
        return True