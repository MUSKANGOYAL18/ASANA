"""Generate task data with LLM-powered descriptions."""
import logging
import random
from typing import List, Optional
from datetime import datetime
from src.models.schema import Task
from src.utils.llm import LLMGenerator
from src.utils.temporal import TemporalGenerator
from src.config import Config
import numpy as np

logger = logging.getLogger(__name__)

class TaskGenerator:
    """Generate realistic task entities."""
    
    def __init__(self, seed: int = 42):
        self.llm = LLMGenerator()
        self.temporal_gen = TemporalGenerator(
            Config.SIMULATION_START_DATE,
            Config.SIMULATION_END_DATE,
            seed=seed
        )
        self.rng = random.Random(seed)
        self.np_rng = np.random.RandomState(seed)
        
    def generate_tasks(self, project_id: str, section_id: str,
                      workflow_type: str, project_type: str,
                      team_members: List[str], project_created_at: datetime,
                      num_tasks: int) -> List[Task]:
        """Generate multiple tasks for a project section."""
        tasks = []
        
        for i in range(num_tasks):
            task = self._generate_single_task(
                project_id, section_id, workflow_type, project_type,
                team_members, project_created_at
            )
            tasks.append(task)
            
        logger.info(f"Generated {num_tasks} tasks for project {project_id}")
        return tasks
        
    def _generate_single_task(self, project_id: str, section_id: str,
                             workflow_type: str, project_type: str,
                             team_members: List[str],
                             project_created_at: datetime) -> Task:
        """Generate a single task with realistic attributes."""
        
        # Generate creation time (after project creation)
        created_at = self.temporal_gen.random_date_in_range(
            project_created_at,
            Config.SIMULATION_END_DATE
        )
        created_at = self.temporal_gen.generate_workday_time(created_at)
        
        # Generate task name using LLM
        context = {
            'project_name': f'{workflow_type.title()} Project',
            'component': self._get_component(workflow_type),
            'campaign': self._get_campaign(workflow_type),
            'feature': self._get_feature(workflow_type)
        }
        
        task_name = self.llm.generate_task_name(project_type, workflow_type, context)
        
        # Generate description with varying detail levels
        detail_level = self.rng.choices(
            ['empty', 'brief', 'detailed'],
            weights=[0.20, 0.50, 0.30]
        )[0]
        
        description = self.llm.generate_task_description(
            task_name, workflow_type, detail_level
        )
        
        # Assign task (85% assigned, 15% unassigned per Asana benchmarks)
        assignee_id = None
        if self.rng.random() < Config.TASK_ASSIGNMENT_RATE and team_members:
            assignee_id = self.rng.choice(team_members)
            
        # Generate due date
        due_date = self.temporal_gen.generate_due_date(
            created_at,
            Config.DUE_DATE_DISTRIBUTION
        )
        
        # Determine completion status
        completion_rate_range = Config.COMPLETION_RATES.get(project_type, (0.50, 0.65))
        completion_rate = self.rng.uniform(*completion_rate_range)
        
        completed = self.rng.random() < completion_rate
        completed_at = None
        completed_by_id = None
        
        if completed:
            completed_at = self.temporal_gen.generate_completion_time(created_at, due_date)
            completed_by_id = assignee_id if assignee_id else self.rng.choice(team_members)
            
        # Generate priority (30% have explicit priority)
        priority = None
        if self.rng.random() < 0.30:
            priority = self.rng.choices(
                ['low', 'medium', 'high', 'urgent'],
                weights=[0.20, 0.50, 0.25, 0.05]
            )[0]
            
        # Select creator
        created_by_id = self.rng.choice(team_members)
        
        task = Task(
            project_id=project_id,
            section_id=section_id,
            name=task_name,
            description=description,
            assignee_id=assignee_id,
            created_by_id=created_by_id,
            created_at=created_at,
            modified_at=completed_at if completed else created_at,
            due_date=due_date,
            completed=completed,
            completed_at=completed_at,
            completed_by_id=completed_by_id,
            priority=priority
        )
        
        return task
        
    def _get_component(self, workflow_type: str) -> str:
        """Get component name for engineering tasks."""
        components = ['API', 'Frontend', 'Backend', 'Database', 'CI/CD', 'Mobile', 'Infrastructure']
        return self.rng.choice(components)
        
    def _get_campaign(self, workflow_type: str) -> str:
        """Get campaign name for marketing tasks."""
        campaigns = ['Q4 Launch', 'Email Campaign', 'Social Media', 'Content Marketing', 'Product Launch']
        return self.rng.choice(campaigns)
        
    def _get_feature(self, workflow_type: str) -> str:
        """Get feature name for product tasks."""
        features = ['Mobile App', 'Dashboard', 'Analytics', 'User Onboarding', 'Notifications']
        return self.rng.choice(features)