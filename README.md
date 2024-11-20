# Peak Performer

**Tagline**: Because you're always on top of the mountain (or at least your to-do list).

## Introduction

Peak Performer is a simple yet robust to-do list application designed to keep you organized and productive. Built with Python and Flask, it leverages best practices in software design, including the Model-View-Controller (MVC) and Repository design patterns, ensuring scalability and maintainability.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
  - [Model-View-Controller (MVC)](#model-view-controller-mvc)
  - [Repository Design Pattern](#repository-design-pattern)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Features

- User authentication (register, login, logout).
- Create, view, edit, and delete tasks.
- Role-based task management.
- API endpoint to fetch task details.
- Persistent data storage using PostgreSQL.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/peak-performer.git
   cd peak-performer

2. Use the provided `run.sh` script to deploy application:
   - Run `initial-setup` to:
     - Create/load the virtual environment
     - Insall depenencies
     - Build PostgreSQL database 
   - 

Load environment variables:
bash
Copy code
./run.sh load-env
Set up a virtual environment and install dependencies:
bash
Copy code
./run.sh install-deps
Initialize the database:
bash
Copy code
./run.sh create-db


## Architecture
### Model-View-Controller (MVC)
- **Model:**
  - Defined in `models.py`, representing `Users` and `Tasks` with SQLAlchemy.
- **View:**
  - HTML templates (e.g., `login.html`, `view_tasks.html`) extend `base.html` for a consistent UI.
  - Built with Bootstrap for responsive and elegant styling.
- **Controller:**
  - Route handling and logic in `auth_controller.py` and `tasks_controller.py`.

#### Benefits:
- Clear separation of concerns.
- Improved maintainability and scalability.
  
## Repository Design Pattern
- **Repositories:**
  - `UsersRepository`: Handles CRUD operations for user accounts.
  - `TasksRepository`: Abstracts database logic for task management.
- **Advantages:**
  - Centralized data access logic.
  - Simplified testing by isolating database operations.
Centralized data access logic.
Simplified testing by isolating database operations.