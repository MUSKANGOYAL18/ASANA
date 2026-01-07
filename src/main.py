"""Main entry point for Asana simulation data generation."""
import logging
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.utils.database import Database
from src.utils.temporal import TemporalGenerator
from src.generators.organization import OrganizationGenerator
from src.generators.users import UserGenerator
from src.scrapers.name_generator import NameGenerator
from src.models.schema import Team, TeamMembership, Project, Section

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AsanaSimulation:
    """Main orchestrator for Asana workspace simulation."""
    
    def __init__(self, db_path: str = None, seed: int = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.seed = seed or Config.RANDOM_SEED
        self.db = Database(self.db_path)
        self.rng = random.Random(self.seed)
        
        # Set random seeds
        random.seed(self.seed)
        
        # Generators
        self.org_gen = OrganizationGenerator(seed=self.seed)
        self.temporal_gen = TemporalGenerator(
            Config.SIMULATION_START_DATE,
            Config.SIMULATION_END_DATE,
            seed=self.seed
        )
        
        # Storage for generated entities
        self.organization = None
        self.teams = []
        self.users = []
        self.projects = []
        
    def run(self):
        """Execute full simulation pipeline."""
        logger.info("=" * 80)
        logger.info("Starting Asana Workspace Simulation")
        logger.info("=" * 80)
        
        try:
            # Validate configuration
            Config.validate()
            
            # Initialize database
            self.db.connect()
            schema_path = Path(__file__).parent.parent / 'schema.sql'
            self.db.initialize_schema(str(schema_path))
            
            # Generate data
            self.generate_organization()
            self.generate_teams()
            self.generate_users()
            self.generate_team_memberships()
            self.generate_projects()
            self.generate_sections()
            self.generate_tasks()
            self.generate_comments()
            self.generate_custom_fields()
            self.generate_tags()
            
            # Final commit
            self.db.commit()
            
            # Print statistics
            self.print_statistics()
            
            logger.info("=" * 80)
            logger.info(f"✓ Simulation complete! Database saved to: {self.db_path}")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Simulation failed: {e}", exc_info=True)
            raise
        finally:
            self.db.close()
            
    def generate_organization(self):
        """Generate organization/workspace."""
        logger.info("Generating organization...")
        self.organization = self.org_gen.generate()
        
        org_data = {
            'organization_id': self.organization.organization_id,
            'name': self.organization.name,
            'domain': self.organization.domain,
            'created_at': self.organization.created_at,
            'is_organization': self.organization.is_organization,
            'settings': self.organization.settings
        }
        
        self.db.insert('organizations', org_data)
        self.db.commit()
        
    def generate_teams(self):
        """Generate teams based on company structure."""
        logger.info("Generating teams...")
        
        team_configs = [
            ('Engineering', 'engineering', 'Software development and infrastructure'),
            ('Product', 'product', 'Product management and design'),
            ('Marketing', 'marketing', 'Marketing and growth'),
            ('Sales', 'sales', 'Sales and business development'),
            ('Operations', 'operations', 'HR, Finance, and Operations')
        ]
        
        for name, team_type, description in team_configs:
            team = Team(
                organization_id=self.organization.organization_id,
                name=name,
                description=description,
                team_type=team_type,
                created_at=Config.SIMULATION_START_DATE
            )
            
            self.teams.append(team)
            
            team_data = {
                'team_id': team.team_id,
                'organization_id': team.organization_id,
                'name': team.name,
                'description': team.description,
                'team_type': team.team_type,
                'created_at': team.created_at
            }
            
            self.db.insert('teams', team_data)
            
        self.db.commit()
        logger.info(f"Generated {len(self.teams)} teams")
        
    def generate_users(self):
        """Generate users distributed across teams."""
        logger.info("Generating users...")
        
        total_users = Config.COMPANY_SIZE
        
        for team in self.teams:
            # Calculate users per team based on distribution
            team_ratio = Config.TEAM_DISTRIBUTION.get(team.team_type, 0.20)
            num_users = int(total_users * team_ratio)
            
            user_gen = UserGenerator(
                self.organization.organization_id,
                self.organization.domain,
                seed=self.seed + hash(team.team_id) % 10000
            )
            
            team_users = user_gen.generate_users(num_users, team.team_type)
            
            # Insert users
            for user in team_users:
                user_data = {
                    'user_id': user.user_id,
                    'organization_id': user.organization_id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role,
                    'job_title': user.job_title,
                    'department': user.department,
                    'created_at': user.created_at,
                    'is_active': user.is_active,
                    'photo_url': user.photo_url
                }
                self.db.insert('users', user_data)
                
            self.users.extend(team_users)
            
        self.db.commit()
        logger.info(f"Generated {len(self.users)} users")
        
    def generate_team_memberships(self):
        """Assign users to teams."""
        logger.info("Generating team memberships...")
        
        memberships = []
        
        for team in self.teams:
            # Get users from this team's department
            team_users = [u for u in self.users if u.department == team.team_type]
            
            for user in team_users:
                # 5% chance of being team lead
                is_team_lead = self.rng.random() < 0.05
                
                membership = TeamMembership(
                    team_id=team.team_id,
                    user_id=user.user_id,
                    joined_at=user.created_at,
                    is_team_lead=is_team_lead
                )
                
                membership_data = {
                    'membership_id': membership.membership_id,
                    'team_id': membership.team_id,
                    'user_id': membership.user_id,
                    'joined_at': membership.joined_at,
                    'is_team_lead': membership.is_team_lead
                }
                
                self.db.insert('team_memberships', membership_data)
                memberships.append(membership)
                
        self.db.commit()
        logger.info(f"Generated {len(memberships)} team memberships")
        
    def generate_projects(self):
        """Generate projects for each team."""
        logger.info("Generating projects...")
        
        # Projects per team (based on team size)
        projects_per_team = {
            'engineering': 25,
            'product': 15,
            'marketing': 20,
            'sales': 10,
            'operations': 10
        }
        
        for team in self.teams:
            num_projects = projects_per_team.get(team.team_type, 10)
            
            for i in range(num_projects):
                # Select project type
                project_type = self.rng.choices(
                    list(Config.PROJECT_TYPE_DISTRIBUTION.keys()),
                    weights=list(Config.PROJECT_TYPE_DISTRIBUTION.values())
                )[0]
                
                # Generate project name
                project_name = self._generate_project_name(team.team_type, i)
                
                # Select owner from team
                team_members = [u.user_id for u in self.users if u.department == team.team_type]
                owner_id = self.rng.choice(team_members) if team_members else None
                
                # Generate creation date
                created_at = self.temporal_gen.random_date_in_range(
                    Config.SIMULATION_START_DATE,
                    Config.SIMULATION_END_DATE - timedelta(days=14)
                )
                
                # 20% of projects have due dates
                due_date = None
                if self.rng.random() < 0.20:
                    due_date = created_at + timedelta(days=self.rng.randint(30, 180))
                    
                project = Project(
                    organization_id=self.organization.organization_id,
                    team_id=team.team_id,
                    name=project_name,
                    description=f"Project for {team.name} team",
                    project_type=project_type,
                    workflow_type=team.team_type,
                    owner_id=owner_id,
                    created_at=created_at,
                    due_date=due_date,
                    color=self.rng.choice(Config.ASANA_COLORS),
                    privacy_setting='team'
                )
                
                self.projects.append(project)
                
                project_data = {
                    'project_id': project.project_id,
                    'organization_id': project.organization_id,
                    'team_id': project.team_id,
                    'name': project.name,
                    'description': project.description,
                    'project_type': project.project_type,
                    'workflow_type': project.workflow_type,
                    'owner_id': project.owner_id,
                    'created_at': project.created_at,
                    'due_date': project.due_date,
                    'is_archived': project.is_archived,
                    'color': project.color,
                    'privacy_setting': project.privacy_setting
                }
                
                self.db.insert('projects', project_data)
                
        self.db.commit()
        logger.info(f"Generated {len(self.projects)} projects")
        
    def generate_sections(self):
        """Generate sections for each project."""
        logger.info("Generating sections...")
        
        sections_count = 0
        
        for project in self.projects:
            # Get section template based on project type
            section_names = Config.SECTION_TEMPLATES.get(
                project.project_type,
                ['To Do', 'In Progress', 'Done']
            )
            
            for position, name in enumerate(section_names):
                section = Section(
                    project_id=project.project_id,
                    name=name,
                    position=position,
                    created_at=project.created_at
                )
                
                section_data = {
                    'section_id': section.section_id,
                    'project_id': section.project_id,
                    'name': section.name,
                    'position': section.position,
                    'created_at': section.created_at
                }
                
                self.db.insert('sections', section_data)
                sections_count += 1
                
        self.db.commit()
        logger.info(f"Generated {sections_count} sections")
        
    def generate_tasks(self):
        """Generate tasks for projects - SIMPLIFIED VERSION."""
        logger.info("Generating tasks (this may take a while)...")
        logger.info("Note: Using simplified task generation for demo purposes")
        
        from src.generators.tasks import TaskGenerator
        
        task_gen = TaskGenerator(seed=self.seed)
        total_tasks = 0
        
        # Limit to first 10 projects for demo
        demo_projects = self.projects[:10]
        
        for project in demo_projects:
            # Get sections for this project
            sections = self.db.query(
                "SELECT section_id FROM sections WHERE project_id = ?",
                (project.project_id,)
            )
            
            if not sections:
                continue
                
            # Get team members
            team_members = [u.user_id for u in self.users 
                          if u.department == project.workflow_type and u.is_active]
            
            if not team_members:
                continue
                
            # Generate 5-15 tasks per section
            tasks_per_section = self.rng.randint(5, 15)
            
            for section_row in sections:
                section_id = section_row[0]
                
                tasks = task_gen.generate_tasks(
                    project.project_id,
                    section_id,
                    project.workflow_type,
                    project.project_type,
                    team_members,
                    project.created_at,
                    tasks_per_section
                )
                
                # Insert tasks
                for task in tasks:
                    task_data = {
                        'task_id': task.task_id,
                        'project_id': task.project_id,
                        'section_id': task.section_id,
                        'parent_task_id': task.parent_task_id,
                        'name': task.name,
                        'description': task.description,
                        'assignee_id': task.assignee_id,
                        'created_by_id': task.created_by_id,
                        'created_at': task.created_at,
                        'modified_at': task.modified_at,
                        'due_date': task.due_date,
                        'start_date': task.start_date,
                        'completed': task.completed,
                        'completed_at': task.completed_at,
                        'completed_by_id': task.completed_by_id,
                        'priority': task.priority,
                        'num_subtasks': task.num_subtasks,
                        'num_comments': task.num_comments,
                        'num_attachments': task.num_attachments
                    }
                    
                    self.db.insert('tasks', task_data)
                    total_tasks += 1
                    
                if total_tasks % 50 == 0:
                    self.db.commit()
                    logger.info(f"Generated {total_tasks} tasks so far...")
                    
        self.db.commit()
        logger.info(f"Generated {total_tasks} tasks total")
        
    def generate_comments(self):
        """Generate comments for tasks."""
        logger.info("Generating comments...")
        logger.info("Skipping comment generation for demo - can be added later")
        
    def generate_custom_fields(self):
        """Generate custom fields."""
        logger.info("Generating custom fields...")
        logger.info("Skipping custom field generation for demo - can be added later")
        
    def generate_tags(self):
        """Generate tags."""
        logger.info("Generating tags...")
        logger.info("Skipping tag generation for demo - can be added later")
        
    def _generate_project_name(self, workflow_type: str, index: int) -> str:
        """Generate realistic project name."""
        templates = {
            'engineering': [
                f'Q{(index % 4) + 1} 2024 Sprint {index + 1}',
                f'Backend Services - Phase {index + 1}',
                f'Mobile App Development',
                f'Infrastructure Improvements',
                f'Bug Fixes & Technical Debt'
            ],
            'product': [
                f'Product Roadmap Q{(index % 4) + 1}',
                f'User Research - {index + 1}',
                f'Feature Planning',
                f'Design System Updates'
            ],
            'marketing': [
                f'Q{(index % 4) + 1} Marketing Campaign',
                f'Content Calendar - {index + 1}',
                f'Social Media Strategy',
                f'Product Launch Materials'
            ],
            'sales': [
                f'Q{(index % 4) + 1} Sales Pipeline',
                f'Enterprise Deals',
                f'Customer Onboarding',
                f'Sales Enablement'
            ],
            'operations': [
                f'Q{(index % 4) + 1} Operations',
                f'HR Initiatives',
                f'Finance Planning',
                f'Team Events & Culture'
            ]
        }
        
        options = templates.get(workflow_type, [f'Project {index + 1}'])
        return self.rng.choice(options)
        
    def print_statistics(self):
        """Print database statistics."""
        stats = self.db.get_stats()
        
        logger.info("\n" + "=" * 80)
        logger.info("DATABASE STATISTICS")
        logger.info("=" * 80)
        
        for table, count in stats.items():
            logger.info(f"{table:.<30} {count:>10,}")
            
        logger.info("=" * 80)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate Asana workspace simulation')
    parser.add_argument('--db-path', type=str, help='Database output path')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--company-size', type=int, help='Number of employees')
    
    args = parser.parse_args()
    
    # Override config if provided
    if args.company_size:
        Config.COMPANY_SIZE = args.company_size
        
    # Run simulation
    sim = AsanaSimulation(
        db_path=args.db_path,
        seed=args.seed
    )
    
    sim.run()

if __name__ == '__main__':
    main()