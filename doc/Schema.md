
                              ┌─────────────────┐
                              │  organizations  │
                              │─────────────────│
                              │ organization_id │ (PK)
                              │ name            │
                              │ domain          │ (UNIQUE)
                              │ created_at      │
                              │ is_organization │
                              │ settings (JSON) │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼    
            ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        
            │    teams     │   │    users     │   │     tags     │
            │──────────────│   │──────────────│   │──────────────│
            │ team_id (PK) │   │ user_id (PK) │   │ tag_id (PK)  │
            │ org_id (FK)  │   │ org_id (FK)  │   │ org_id (FK)  │
            │ name         │   │ email (UNIQ) │   │ name         │
            │ team_type    │   │ name         │   │ color        │
            │ description  │   │ role         │   │ created_at   │
            │ created_at   │   │ job_title    │   └──────────────┘
            └──────┬───────┘   │ department   │
                   │           │ is_active    │
                   │           │ created_at   │
                   │           └──────┬───────┘
                   │                  │
                   └──────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  team_memberships     │
              │───────────────────────│
              │ membership_id (PK)    │
              │ team_id (FK)          │
              │ user_id (FK)          │
              │ joined_at             │
              │ is_team_lead          │
              │ UNIQUE(team_id,       │
              │        user_id)       │
              └───────────────────────┘

                                                
            ┌──────────────┐
            │   projects   │
            │──────────────│
            │ project_id   │ (PK)
            │ org_id (FK)  │
            │ team_id (FK) │
            │ name         │
            │ description  │
            │ project_type │
            │ workflow_type│
            │ owner_id (FK)│ → users
            │ created_at   │
            │ due_date     │
            │ is_archived  │
            │ color        │
            └──────┬───────┘
                   │
                   ▼
            
            ┌──────────────┐
            │   sections   │
            │──────────────│
            │ section_id   │ (PK)
            │ project_id   │ (FK)
            │ name         │
            │ position     │
            │ created_at   │
            │ UNIQUE(proj, │
            │        pos)  │
            └──────┬───────┘
                   │
                   ▼
            ┌──────────────────────────┐
            │         tasks            │
            │──────────────────────────│
            │ task_id (PK)             │
            │ project_id (FK)          │
            │ section_id (FK)          │
            │ parent_task_id (FK)      │ → tasks (self-ref)
            │ name                     │
            │ description              │
            │ assignee_id (FK)         │ → users
            │ created_by_id (FK)       │ → users
            │ created_at               │
            │ modified_at              │
            │ due_date                 │
            │ start_date               │
            │ completed                │
            │ completed_at             │
            │ completed_by_id (FK)     │ → users
            │ priority                 │
            │ num_subtasks             │
            │ num_comments             │
            │ num_attachments          │
            └────────┬─────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┬──────────────┐
        │            │            │              │              │
        ▼            ▼            ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐
│ comments │ │task_tags │ │custom_   │ │ attachments  │ │ (subtask)│
│──────────│ │──────────│ │field_    │ │──────────────│ │ parent   │
│comment_id│ │task_id   │ │values    │ │attachment_id │ │ reference│
│task_id   │ │tag_id    │ │──────────│ │task_id       │ └──────────┘
│user_id   │ │added_at  │ │value_id  │ │uploaded_by   │
│text      │ │PK(task,  │ │task_id   │ │filename      │
│created_at│ │   tag)   │ │field_id  │ │file_type     │
│type      │ └──────────┘ │value     │ │file_size     │
└──────────┘              │UNIQUE(   │ │url           │
                          │task,fld) │ │created_at    │
                          └──────────┘ └──────────────┘
                                 ▲
                                 │
                          ┌──────┴──────────┐
                          │ custom_field_   │
                          │ definitions     │
                          │─────────────────│
                          │ field_id (PK)   │
                          │ org_id (FK)     │
                          │ project_id (FK) │
                          │ name            │
                          │ field_type      │
                          │ description     │
                          │ created_at      │
                          │ enum_options    │
                          │ (JSON)          │
                          └─────────────────┘