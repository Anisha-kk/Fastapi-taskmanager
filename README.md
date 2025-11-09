# Overview

The Task Manager REST API is a backend service built with FastAPI that allows users to register, log in, and manage their personal tasks.


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
├── frontend/
│   ├── index.html
├── requirements.txt
├── venv
└── README.md

## Tables Overview
Table	Description
users	Stores user info and roles for authentication
tasks	Stores task info linked to users

### Users Table
Column	        Type	    Constraints
username        VARCHAR	    Primary key
email	        VARCHAR	    Unique, Not Null
hashed_password	VARCHAR	    Not Null
is_active       Boolean

### Tasks Table
Column	    Type	    Constraints
id	        Integer	    Primary Key
title	    VARCHAR	    Not Null
description	VARCHAR	    Optional
status	    TEXT        Values: pending (default)/in_progress/completed/archieved
priority	TEXT        Values: low/medium(default)/high/urgent
due_date    TIMESTAMP
created_at	TIMESTAMP	Default CURRENT_TIMESTAMP
updated_at	TIMESTAMP	Default CURRENT_TIMESTAMP
ownername   VARCHAR     Foreign key from user table


### Result
When run in local: 
    Html frontend shown in 127.0.0.0:8000
    Swagger docs in 127.0.0.0:8000/docs