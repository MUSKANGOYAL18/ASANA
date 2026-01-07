

CREATE TABLE IF NOT EXISTS organizations (
    organization_id TEXT PRIMARY KEY,      -- UUID format (simulating Asana GID)
    name TEXT NOT NULL,                     -- Company name
    domain TEXT NOT NULL UNIQUE,            -- Email domain (e.g., acme.com)
    created_at TIMESTAMP NOT NULL,
    is_organization BOOLEAN NOT NULL DEFAULT 1,  -- TRUE for verified domains
    settings JSON                           -- Workspace settings (JSON blob)
);

CREATE INDEX idx_org_domain ON organizations(domain);



CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    team_type TEXT NOT NULL,   -- 'engineering', 'product', 'marketing', 'sales', 'operations'
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

CREATE INDEX idx_team_org ON teams(organization_id);
CREATE INDEX idx_team_type ON teams(team_type);


CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    role TEXT NOT NULL,          -- 'admin', 'member', 'guest'
    job_title TEXT,
    department TEXT,
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    photo_url TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

CREATE INDEX idx_user_org ON users(organization_id);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_active ON users(is_active);


CREATE TABLE IF NOT EXISTS team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    is_team_lead BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE (team_id, user_id)
);

CREATE INDEX idx_membership_team ON team_memberships(team_id);
CREATE INDEX idx_membership_user ON team_memberships(user_id);


CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    team_id TEXT,                -- Can be NULL for cross-team projects
    name TEXT NOT NULL,
    description TEXT,
    project_type TEXT NOT NULL,  -- 'sprint', 'kanban', 'timeline', 'calendar', 'list'
    workflow_type TEXT NOT NULL, -- 'engineering', 'marketing', 'product', 'operations'
    owner_id TEXT,               -- Project owner
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    color TEXT,                  -- Asana color (e.g., 'light-green', 'dark-blue')
    privacy_setting TEXT NOT NULL DEFAULT 'team',  -- 'public', 'team', 'private'
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE INDEX idx_project_org ON projects(organization_id);
CREATE INDEX idx_project_team ON projects(team_id);
CREATE INDEX idx_project_type ON projects(project_type);
CREATE INDEX idx_project_archived ON projects(is_archived);


CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,   -- Order within project
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE (project_id, position)
);

CREATE INDEX idx_section_project ON sections(project_id);


CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,             -- Can be NULL (unassigned to section)
    parent_task_id TEXT,         -- NULL for top-level tasks, set for subtasks
    name TEXT NOT NULL,
    description TEXT,            -- Rich text (can include markdown)
    assignee_id TEXT,            -- Can be NULL (unassigned)
    created_by_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    modified_at TIMESTAMP NOT NULL,
    due_date DATE,
    start_date DATE,
    completed BOOLEAN NOT NULL DEFAULT 0,
    completed_at TIMESTAMP,
    completed_by_id TEXT,
    priority TEXT,               -- 'low', 'medium', 'high', 'urgent'
    num_subtasks INTEGER NOT NULL DEFAULT 0,
    num_comments INTEGER NOT NULL DEFAULT 0,
    num_attachments INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by_id) REFERENCES users(user_id),
    FOREIGN KEY (completed_by_id) REFERENCES users(user_id),    
    CHECK (completed = 0 OR completed_at IS NOT NULL),
    CHECK (parent_task_id IS NULL OR section_id IS NULL)  -- Subtasks inherit section
);

CREATE INDEX idx_task_project ON tasks(project_id);
CREATE INDEX idx_task_section ON tasks(section_id);
CREATE INDEX idx_task_parent ON tasks(parent_task_id);
CREATE INDEX idx_task_assignee ON tasks(assignee_id);
CREATE INDEX idx_task_due_date ON tasks(due_date);
CREATE INDEX idx_task_completed ON tasks(completed);
CREATE INDEX idx_task_created_at ON tasks(created_at);


CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    comment_type TEXT NOT NULL DEFAULT 'comment',  -- 'comment', 'system', 'attachment'
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_comment_task ON comments(task_id);
CREATE INDEX idx_comment_user ON comments(user_id);
CREATE INDEX idx_comment_created ON comments(created_at);


CREATE TABLE IF NOT EXISTS custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    project_id TEXT,             -- NULL for global fields, set for project-specific
    name TEXT NOT NULL,
    field_type TEXT NOT NULL,    -- 'text', 'number', 'enum', 'date', 'people'
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    enum_options JSON,           -- For 'enum' type: ["Option 1", "Option 2", ...]
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE INDEX idx_custom_field_org ON custom_field_definitions(organization_id);
CREATE INDEX idx_custom_field_project ON custom_field_definitions(project_id);

CREATE TABLE IF NOT EXISTS custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    value TEXT,                  -- Stored as text, interpreted based on field_type
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    UNIQUE (task_id, field_id)
);

CREATE INDEX idx_custom_value_task ON custom_field_values(task_id);
CREATE INDEX idx_custom_value_field ON custom_field_values(field_id);




CREATE TABLE IF NOT EXISTS tags (
    tag_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    UNIQUE (organization_id, name)
);

CREATE INDEX idx_tag_org ON tags(organization_id);

CREATE TABLE IF NOT EXISTS task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TIMESTAMP NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

CREATE INDEX idx_task_tags_task ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag ON task_tags(tag_id);



CREATE TABLE IF NOT EXISTS attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    uploaded_by_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT,          -- MIME type
    file_size INTEGER,       -- Bytes
    url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by_id) REFERENCES users(user_id)
);

CREATE INDEX idx_attachment_task ON attachments(task_id);
CREATE INDEX idx_attachment_user ON attachments(uploaded_by_id);



