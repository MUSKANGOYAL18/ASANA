
# Asana Workspace Simulation – Seed Data Generator

A production-grade data generator for creating realistic Asana workspace
simulations used as seed data for reinforcement learning (RL) environments.

This project generates a complete SQLite database representing a B2B SaaS
company (5,000–10,000 employees) using Asana for product development,
marketing, and operations workflows.

---

## Overview

This simulation creates realistic seed data for:

- Organizations / Workspaces  
- Teams (Engineering, Product, Marketing, Sales, Operations)  
- Users with realistic demographics  
- Projects across different workflows  
- Tasks with natural language descriptions  
- Subtasks, comments, custom fields, and tags  
- Temporal and relational consistency across all entities  

The generated dataset is designed to resemble real enterprise Asana usage
patterns and is suitable for evaluating and training computer-use AI agents.

---

## Key Features

- **Realistic data sources**  
  Company names and user demographics derived from public datasets and
  industry distributions.

- **LLM-assisted content generation**  
  Task names, descriptions, and comments are generated using prompt-based
  language models (optional and configurable).

- **Research-backed distributions**  
  Task completion rates, due dates, sprint timelines, and team sizes follow
  real-world productivity benchmarks.

- **Temporal consistency**  
  All timestamps obey logical constraints  
  (created_at ≤ completed_at ≤ simulation end).

- **Relational integrity**  
  Foreign keys and business logic enforce realistic Asana relationships.

---

## Prerequisites

- Python 3.9 or higher
- (Optional) API key for an LLM provider if text generation is enabled

---

## Installation

```bash
# Clone the repository
git clone https://github.com/MUSKANGOYAL18/ASANA.git
cd ASANA

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env if LLM-based generation is enabled
