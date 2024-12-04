# Flask Book Exchange Project

## Project Overview

This project is a **Flask-based web application** featuring an admin panel that allows CRUD operations on multiple database tables (`Users`, `Inventory`, `Prompts`, `Transactions`, and `ChatMessages`). It supports authentication, role-based access, and responsive design using **Bootstrap**. Enhanced table functionalities, such as sorting, searching, and pagination, are implemented with **DataTables**.

---

## Features

### Core Features
- **User Authentication**:
  - Secure login/logout functionality.
  - Role-based access control for `Admin` and `User` roles.
- **Admin Panel**:
  - Manage data for `Users`, `Inventory`, `Prompts`, `Transactions`, and `ChatMessages`.
  - CRUD operations for all tables.
  - Integration of **DataTables** for search, sort, and pagination.
- **Responsive Design**:
  - Mobile-friendly layout using **Bootstrap**.
- **Dynamic Tables**:
  - All tables dynamically fetch data from the database.
- **AI feature**:
  - Prompting using LLM ollama model.
  - file and book upload posibility
- **Book exchange**:
  - Users can exchange books between themselves
  - They can upload a book for a exchange  

---

## Tech Stack

### Backend
- **Python**: Programming language.
- **Flask**: Web framework.
- **SQLAlchemy**: ORM for database management.
- **Flask-Migrate**: Database migrations with Alembic.

### Frontend
- **Bootstrap**: For responsive design.
- **DataTables**: For table enhancements like sorting, searching, and pagination.

### Database
- **PostgreSQL**: Relational database for storing application data.

---

## Installation and Setup

### 1. Clone the Repository

```bash
Unzip a project
cd my-dir

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

CREATE DATABASE your_db_name;

Update your config file with db credentials, ollama model endpoint, SQLALCHEMY_DATABASE_URI.

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

flask run # to start a server
