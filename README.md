# Asana Workspace Simulation - Seed Data Generator

A production-grade data generator for creating realistic Asana workspace simulations for RL environment training. This project generates a complete SQLite database representing a B2B SaaS company (5000-10000 employees) using Asana for project management.

## Overview

This simulation creates realistic seed data for:
- Organizations/Workspaces
- Teams (Engineering, Product, Marketing, Sales, Operations)
- Users with realistic demographics
- Projects across different workflows
- Tasks with natural language descriptions
- Subtasks, comments, custom fields, tags
- Temporal and relational consistency

## Features

- **Real-world data sources**: Scraped company names, census-based user demographics
- **LLM-powered content**: Natural task descriptions using GPT-4
- **Research-backed distributions**: Task completion rates, due dates, team sizes based on industry benchmarks
- **Temporal consistency**: All timestamps logically ordered (created < completed < now)
- **Relational integrity**: Foreign keys, business logic validation

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key (for LLM content generation)

### Installation


# Clone the repository
cd asana-simulation

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY




## Usage

### Generate Complete Database


python src/main.py


This will:
1. Scrape real-world data (company names, user demographics)
2. Generate organizational structure (teams, users)
3. Create projects with realistic workflows
4. Generate tasks with LLM-powered descriptions
5. Add subtasks, comments, custom fields, tags
6. Output `asana_simulation.sqlite` in the `output/` directory

### Generate Specific Components


# Generate only users
python src/main.py --only users

# Generate with custom size
python src/main.py --company-size 5000

# Dry run (no database write)
python src/main.py --dry-run
```

## Project Structure


asana-simulation/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── schema.sql                   # Complete DDL for SQLite
├── .env.example                 # Environment template
├── src/
│   ├── main.py                  # Entry point / orchestration
│   ├── config.py                # Configuration management
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── company_scraper.py   # Y Combinator companies
│   │   ├── name_generator.py    # Census-based names
│   │   └── template_scraper.py  # Asana templates
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── organization.py      # Workspace generation
│   │   ├── teams.py             # Team structure
│   │   ├── users.py             # User profiles
│   │   ├── projects.py          # Project creation
│   │   ├── tasks.py             # Task generation
│   │   ├── subtasks.py          # Subtask creation
│   │   ├── comments.py          # Comment generation
│   │   ├── custom_fields.py     # Custom field setup
│   │   └── tags.py              # Tag creation
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py            # Data models
│   └── utils/
│       ├── __init__.py
│       ├── database.py          # SQLite operations
│       ├── llm.py               # OpenAI API calls
│       ├── temporal.py          # Date/time utilities
│       └── distributions.py     # Statistical distributions
├── prompts/
│   ├── task_engineering.txt     # Engineering task prompts
│   ├── task_marketing.txt       # Marketing task prompts
│   ├── task_product.txt         # Product task prompts
│   └── comment_generation.txt   # Comment prompts
├── docs/
│   └── METHODOLOGY.md           # Detailed methodology doc
└── output/
    └── asana_simulation.sqlite  # Generated database
```


### Validation


# Run validation checks
python src/utils/validate.py output/asana_simulation.sqlite


