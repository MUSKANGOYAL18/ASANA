"""Data models for Asana entities."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid

def generate_gid() -> str:
    """Generate Asana-style GID (UUID without hyphens)."""
    return str(uuid.uuid4()).replace('-', '')

@dataclass
class Organization:
    organization_id: str = field(default_factory=generate_gid)
    name: str = ""
    domain: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_organization: bool = True
    settings: dict = field(default_factory=dict)

@dataclass
class Team:
    team_id: str = field(default_factory=generate_gid)
    organization_id: str = ""
    name: str = ""
    description: str = ""
    team_type: str = ""  # engineering, product, marketing, sales, operations
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class User:
    user_id: str = field(default_factory=generate_gid)
    organization_id: str = ""
    email: str = ""
    name: str = ""
    role: str = "member"  # admin, member, guest
    job_title: str = ""
    department: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    photo_url: str = ""

@dataclass
class TeamMembership:
    membership_id: str = field(default_factory=generate_gid)
    team_id: str = ""
    user_id: str = ""
    joined_at: datetime = field(default_factory=datetime.now)
    is_team_lead: bool = False

@dataclass
class Project:
    project_id: str = field(default_factory=generate_gid)
    organization_id: str = ""
    team_id: Optional[str] = None
    name: str = ""
    description: str = ""
    project_type: str = "list"  # sprint, kanban, timeline, calendar, list
    workflow_type: str = ""  # engineering, marketing, product, operations
    owner_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    is_archived: bool = False
    color: str = "light-blue"
    privacy_setting: str = "team"

@dataclass
class Section:
    section_id: str = field(default_factory=generate_gid)
    project_id: str = ""
    name: str = ""
    position: int = 0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    task_id: str = field(default_factory=generate_gid)
    project_id: str = ""
    section_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    name: str = ""
    description: str = ""
    assignee_id: Optional[str] = None
    created_by_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    completed_by_id: Optional[str] = None
    priority: Optional[str] = None
    num_subtasks: int = 0
    num_comments: int = 0
    num_attachments: int = 0

@dataclass
class Comment:
    comment_id: str = field(default_factory=generate_gid)
    task_id: str = ""
    user_id: str = ""
    text: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    comment_type: str = "comment"

@dataclass
class CustomFieldDefinition:
    field_id: str = field(default_factory=generate_gid)
    organization_id: str = ""
    project_id: Optional[str] = None
    name: str = ""
    field_type: str = "text"  # text, number, enum, date, people
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    enum_options: Optional[List[str]] = None

@dataclass
class CustomFieldValue:
    value_id: str = field(default_factory=generate_gid)
    task_id: str = ""
    field_id: str = ""
    value: str = ""

@dataclass
class Tag:
    tag_id: str = field(default_factory=generate_gid)
    organization_id: str = ""
    name: str = ""
    color: str = "light-blue"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TaskTag:
    task_id: str = ""
    tag_id: str = ""
    added_at: datetime = field(default_factory=datetime.now)

@dataclass
class Attachment:
    attachment_id: str = field(default_factory=generate_gid)
    task_id: str = ""
    uploaded_by_id: str = ""
    filename: str = ""
    file_type: str = ""
    file_size: int = 0
    url: str = ""
    created_at: datetime = field(default_factory=datetime.now)