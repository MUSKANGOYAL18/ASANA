This document provides a comprehensive, column-by-column breakdown of the data generation straegy for Asana workspace simulation.

Table of Contents
1. Organizations
2. Teams
3. Users
4. Team Memberships
5. Projects
6. Sections
7. Tasks
8. Comments
9. Custom Fields
10. Tags

**Organizations**

**Represent top level workspace/organization entity**

Column	               Data Type          Source Strategy                                           Methodology & Justification

organization_id        Text(UUID)         Generated                  UUIDv4 generation with hyphens removed to simulate Asana’s GID format. Uses Python’s uuid.uuid4()

name	               TEXT	              Scraped	                 Company names from real B2B Saas companies. Source: Curated list of 50 real companies. Fallback list ensures
                                                                     Fallback list ensures consistent, recognizable company names.

domain	               TEXT	              Derived                    Email domain derived from company name (e.g., “Stripe” → “stripe.com).Lowercase, spaces removed, normalized to 
                                                                     .com TLD

created_at	           TIMESTAMP	      Synthetic                  Set to SIMULATION_START_DATE (default: 6 months ago). Represents when company started using Asana.

is_organization        BOOLEAN	          Constant                   Always TRUE for verified domain organizations (vs. personal workspaces)

settings	           JSON	              Synthetic	                 JSON blob with workspace settings: {"default_view": "list", "color_coding_enabled": true, 
                                                                     "time_tracking_enabled": true}

**Teams**
**Organizational units within the company (Engineering, Marketing, etc.)**
Column	               Data Type          Source Strategy                                           Methodology & Justification

team_id	               TEXT (UUID)	      Generated	                            UUIDv4 generation (hyphens removed)
organization_id	       TEXT (FK)	      Derived	                            Foreign key to parent organization
name	               TEXT	              Constant	                            Fixed team names:“Engineering”, “Product”, “Marketing”, “Sales”, “Operations”.
description	           TEXT	              Template	                            Simple descriptions:“Software development and infrastructure”, “Marketing and growth”, etc.
team_type	           TEXT	              Constant                              Enum: engineering, product, marketing, sales, operations. Used for downstream logic (user 
                                                                                distribution, project types)
created_at	           TIMESTAMP	      Synthetic                             Set to SIMULATION_START_DATE. Teams created when organization started using Asana.

Team Distribution Research:
Engineering: 35% (largest team in tech companies)
Sales: 25% (significant for B2B SaaS)
Marketing: 15%
Operations: 15% (HR, Finance, Legal)
Product: 10%

**Users**
Column	               Data Type          Source Strategy                                           Methodology & Justification

user_id	               TEXT (UUID)	      Generated	                            UUIDv4 generation (hyphens removed)
organization_id	       TEXT (FK)	      Derived	                            Foreign key to parent organization
email	               TEXT	              Generated                             Email generated from name using census-based patterns.Patterns: 70% firstname.lastname@domain
                                                                                , 20% flastname@domain, 10% firstnamel@domain. Ensures realistic email distribution

name	               TEXT	              Scraped                               Source: US Census Bureau name frequency data (2020).Top 100 first names (male/female) and top 100
                                                                                last names.
                                                                                Justification: Reflects realistic demographic distribution in US workforce.
                                                                                50/50 gender split in name selection.

role	               TEXT	              Synthetic                             Enum: admin, member, guest. Distribution: 5% admin, 95% member (based on typical Asana workspace)
job_title	           TEXT	              Template + Heuristics                 Job titles assigned based on department.(Software Engineer, Senior Engineer, Tech Lead, etc.)
department	           TEXT	              Derived                               Matches team type (engineering, product, etc.). Used for team membership assignment
created_at	           TIMESTAMP	      Synthetic                             Join date spread over company history (6 months).Uses uniform distribution with constraint:
                                                                                at least 30 days before SIMULATION_END_DATE to ensure users have activity history
is_active	           BOOLEAN	          Synthetic                             Distribution: 98% active, 2% inactive.
photo_url	           TEXT	              Generated                             Placeholder avatar URLs using pravatar.cc service:https://i.pravatar.cc/150?u={email}. Provides    
                                                                                consistent, unique avatars

User Generation Methodology:
1.Calculate users per team based on TEAM_DISTRIBUTION percentages
2.For each user:
  Generate name from census data (weighted by frequency)
  Create email from name + company domain
  Assign job title from department-specific list
  Generate join date (uniform distribution over 6-month history)
  Assign role (5% admin probability)
  Set active status (98% active)

**Team Memberships**
Many-to-many relationship between users and teams.

Column	               Data Type          Source Strategy                                           Methodology & Justification
membership_id	       TEXT (UUID)	      Generated	                            UUIDv4 generation
team_id	               TEXT (FK)	      Derived	                            Foreign key to team
user_id	               TEXT (FK)	      Derived	                            Foreign key to user
joined_at	           TIMESTAMP	      Derived                               Set to user's created_at (users join their primary team when they join company)
is_team_lead	       BOOLEAN	          Synthetic                             Distribution: 5% team leads per team.
                                                                                Justification: Typical ratio of 1 lead per 20 team members in flat organizations

Consistency Rules:
Users only join teams matching their department
joined_at always equals user’s created_at
Unique constraint on (team_id, user_id)

**Projects**
Collections of tasks organized around goals/initiatives.
Column	               Data Type          Source Strategy                                           Methodology & Justification

project_id	           TEXT (UUID)	      Generated	                            UUIDv4 generation
organization_id	       TEXT (FK)	      Derived	                            Foreign key to organization
team_id	               TEXT (FK)	      Derived	                            Foreign key to owning team
name	               TEXT	              Template + Heuristics                 Project names follow team-specific patterns.
description	           TEXT	              Template                              Simple description: "Project for {team_name} team"
project_type	       TEXT	              Synthetic                             Enum: sprint, kanban, timeline, calendar, list.  Distribution (based on Asana usage patterns): 
                                                                                Sprint 30%, Kanban 25%, Timeline 20%, List 20%, Calendar 5%
workflow_type	       TEXT	              Derived                               Matches team type (engineering, marketing, etc.)
owner_id	           TEXT (FK)	      Derived	                            Random team member selected as project owner
created_at	           TIMESTAMP	      Synthetic                             Random date between SIMULATION_START_DATE and 14 days before SIMULATION_END_DATE.
due_date	           DATE	              Synthetic                             Distribution: 20% of projects have due dates (80% are ongoing). Due dates are 30-180 days after 
                                                                                creation (based on typical project timelines)
is_archived	           BOOLEAN	          Constant                              Always FALSE in initial simulation (archived projects can be added in future iterations)
color	               TEXT	              Synthetic                             Random selection from Asana’s 18 color palette: light-pink, dark-blue, etc.
privacy_setting	       TEXT	              Constant	                            Always team (projects visible to team members)


Project Count per Team:
Engineering: 25 projects (most active)
Marketing: 20 projects
Product: 15 projects
Sales: 10 projects
Operations: 10 projects
Total: ~80 projects for 7,500-person company (realistic ratio)

**Sections**
Subdivisions within projects (columns in Kanban, stages in workflow).

Column	               Data Type          Source Strategy                                           Methodology & Justification

section_id	           TEXT (UUID)	      Generated	                            UUIDv4 generation
project_id	           TEXT (FK)	      Derived	                            Foreign key to parent project
name	               TEXT	              Template	                            Section names based on project type. Source: Asana’s default templates.
                                                                                Sprint: ["Backlog", "To Do", "In Progress", "In Review", "Done"].
                                                                                Kanban: ["To Do", "In Progress", "Done"].
                                                                                Timeline: ["Planning", "Execution", "Review", "Complete"]

position	           INTEGER	          Derived                               Sequential integer (0, 1, 2, …) representing order within project
created_at	           TIMESTAMP	      Derived                               Set to project’s created_at (sections created with project)

Consistency Rules:

Sections created in order (position 0, 1, 2, …)
Unique constraint on (project_id, position)
All sections created at same time as project

**Tasks**
The fundamental unit of work in Asana.
Column	               Data Type          Source Strategy                                           Methodology & Justification

task_id	               TEXT (UUID)	      Generated	                            UUIDv4 generation
project_id	           TEXT (FK)	      Derived	                                Foreign key to parent project
section_id	           TEXT (FK)	      Derived	                                Foreign key to section within project
parent_task_id	       TEXT (FK)	      Derived                                  NULL for top-level tasks, set for subtasks. Distribution: 20% of tasks have 
                                                                                subtasks (1-5 subtasks each)
name	               TEXT	              LLM + Heuristics                        LLM Generation: Task names generated via GPT-4 with prompts tailored to  
                                                                                project type.
                                                                                Engineering tasks follow pattern: "[Component]-[Action]-[Detail]" (e.g., "API - Implement - User authentication endpoint").
                                                                                Marketing tasks follow: "[Campaign] - [Deliverable]" (e.g., "Q4 Launch - Create landing page copy").
                                                                                Product tasks: "[Activity] - [Detail]" (e.g., “User Research - Conduct interviews with 10 customers”). 
                                                                                Prompts include project context (name, type, workflow) and few-shot examples.
                                                                                Temperature: 0.8 for variety. 
                                                                                Fallback: Template-based generation if LLM fails
description	           TEXT	              LLM + Templates                       Rich text descriptions generated with varying lengths.Distribution: 20% empty, 50% brief (1-3 
                                                                                sentences), 30% detailed (multiple paragraphs with bullet points).
                                                                                LLM Prompt: “Generate a realistic task description for: ‘{task_name}’.Context: This is a {workflow_type} task. Detail level: {brief/detailed}. Use professional tone and markdown formatting.” 
                                                                                Justification: Mirrors real Asana usage where many tasks have minimal descriptions
assignee_id	           TEXT (FK)	      Derived                                 Assigned based on team membership. Distribution: 85% of tasks assigned, 15% unassigned. 
created_by_id	       TEXT (FK)	      Derived	                                  Random team member selected as task creator
created_at	           TIMESTAMP	      Synthetic                             Random date between project creation and SIMULATION_END_DATE.
modified_at	           TIMESTAMP	      Derived                               If task completed: completed_at
due_date	           DATE	              Synthetic + Heuristics                25% within 1 week, 40% within 1 month
start_date	           DATE	              Synthetic                             NULL for most tasks. When set, 1-7 days before due_date
completed	           BOOLEAN	          Synthetic + Heuristics                 Sprint projects 70-85%, Kanban 60-75%, Timeline 55-70%, List 50-65%, Calendar 65-80%.
completed_at	       TIMESTAMP	      Derived                               If completed, timestamp generated
completed_by_id	       TEXT (FK)	      Derived                               If completed: assignee (if assigned) or random team member
priority	           TEXT	              Synthetic                             Enum: low, medium, high, urgent
num_subtasks	       INTEGER	          Synthetic                             Updated after subtask generation
num_comments	       INTEGER	          Synthetic                             Updated after comment generation
num_attachments	       INTEGER	          Synthetic                             Updated after attachment generation

Task Generation Methodology:
1.For each project section:
  Generate 5-15 tasks (random)
2.For each task:
  Generate creation timestamp (workday hours, weighted by day of week)
  Call LLM to generate task name (with project context)
  Determine description detail level (20% empty, 50% brief, 30% detailed)
  Call LLM to generate description (if not empty)
  Assign to team member (85% probability)
  Generate due date (following distribution)
  Determine completion status (based on project type completion rate)
  If completed: generate completion timestamp (log-normal distribution)
  Generate priority (30% probability)

assignee_id must be team member
created_by_id must be team member
section_id must belong to project_id

**Comments**
Activity and discussion on tasks.

Column	               Data Type          Source Strategy                                           Methodology & Justification
comment_id	           TEXT (UUID)	      Generated	                            UUIDv4 generation
task_id	               TEXT (FK)	      Derived	                            Foreign key to parent task
user_id	               TEXT (FK)	      Derived	                            Random team member 
text	               TEXT	              LLM                                   Comments generated via GPT-4
created_at	           TIMESTAMP	      Synthetic                             Random timestamp between task created_at and completed_at
comment_type	       TEXT	              Synthetic	                            comment, system, attachment

**Custom Fields**
User-defined fields for tracking additional metadata.

Column	               Data Type          Source Strategy                                           Methodology & Justification

field_id	           TEXT (UUID)	      Generated	                            UUIDv4 generation
organization_id	       TEXT (FK)	      Derived	                            Foreign key to organization
project_id	           TEXT (FK)	      Derived	                            NULL for global fields, set for project-specific fields.
name	               TEXT	              Template                              Common custom field names.
field_type	           TEXT	              Synthetic	                            Enum: text, number, enum, date, people
description	           TEXT	              Template                              Simple descriptions: “Track story points for estimation”, “Assign to sprint”, etc.
created_at	           TIMESTAMP	      Derived	                            Set to project created_at

Custom Field Methodology:
Create 3-5 custom fields per project

**Tags**
Column	               Data Type          Source Strategy                                           Methodology & Justification
tag_id	               TEXT (UUID)	      Generated	                            UUIDv4 generation
organization_id	       TEXT (FK)	      Derived	                            Foreign key to organization
name	               TEXT	              Template                              Common tag names. Examples: “urgent”, “blocked”
created_at	           TIMESTAMP	      Synthetic	                            Random date between organization creation and 30 days ago

Tag Methodology:
Create 15-20 organization-level tags



















