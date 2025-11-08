# Overview

The Task Manager REST API is a backend service built with FastAPI that allows users to register, log in, and manage their personal tasks.
It demonstrates authentication, CRUD operations, database design, containerization, testing, and CI/CD integration, making it ideal for backend or Python developer portfolios.

## Tech Stack

Language: Python 3.11
Framework: FastAPI
Database: PostgreSQL (via SQLAlchemy ORM)
Auth: JWT (using python-jose)
Testing: pytest + FastAPI TestClient

## Project structure

fastapi-taskmanager/
│
├── app/
│   ├── main.py
│   ├── __init__.py
│   ├── core/
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   └── tests/
|       ├── test_root.py 
│       ├── test_auth.py
│       └── test_tasks.py
│
|── logger/
│   ├── __init__.py
|   ├── logger.conf
|   ├── logger.py
|
── logs/
│   ├── access.log
|   ├── db.log
|   ├── error.log
|   ├── info.log
|   ├── server.log                                                                                 
|
├── frontend/
│   ├── index.html
├── requirements.txt
├── venv
└── README.md
python -m venv venv - to create venv
venv\Scripts\activate in cmd
Test code execution: python -m pytest


Refer my previous files in github

pip install -r requirements.txt

## Tables Overview
Table	Description
users	Stores user info and roles for authentication
tasks	Stores task info linked to users

### Users Table
Column	Type	Constraints
id	SERIAL / Integer	Primary Key
username	VARCHAR	Unique, Not Null
email	VARCHAR	Unique, Not Null
hashed_password	VARCHAR	Not Null
role	VARCHAR	Default 'user', can be 'admin'
created_at	TIMESTAMP	Default CURRENT_TIMESTAMP

### Tasks Table
Column	Type	Constraints
id	SERIAL / Integer	Primary Key
title	VARCHAR	Not Null
description	TEXT	Optional
completed	BOOLEAN	Default False
owner_id	Integer	Foreign Key → users.id
created_at	TIMESTAMP	Default CURRENT_TIMESTAMP
updated_at	TIMESTAMP	Updated automatically



Html frontend shown in 127.0.0.0:8000
Swagger docs in 127.0.0.0:8000/docs