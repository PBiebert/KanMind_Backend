# KanMind – Backend

> Kanban-based project management tool | REST API built with Django & Django
> REST Framework

KanMind is a modern project management tool that allows tasks to be organized
clearly in boards and columns. This repository contains **the backend only**,
which provides all data and business logic through a REST API. The corresponding
frontend communicates with this backend via these endpoints.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation & Configuration](#installation--configuration)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Author](#author)

---

## Prerequisites

- Python 3.14.3+
- pip 26.1.1+

---

## Installation & Configuration

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd KanMind_Backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Mac/Linux
   .venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file – sensitive settings are not stored directly in
   `core/settings.py` but loaded from a local `.env` file (ignored by Git):

   ```bash
   cp .env.template .env
   ```

5. Generate a new `SECRET_KEY` and add it to the `.env` file:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Add the generated key and the following values to your `.env` file:

   ```env
   SECRET_KEY='your_generated_key_here'
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   > **Note:** Use `DEBUG=True` for local development only. Set it to `False` in
   > production and update `ALLOWED_HOSTS` to match your actual domain.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://127.0.0.1:8000/`

---

## Project Structure

```
01_DEV/
├── core/               # Django project configuration (settings, urls, wsgi)
├── accounts/           # User management & authentication
│   └── api/            # Serializers, views, URLs for accounts
├── kan_mind/           # Core logic: boards, columns, tasks
│   └── api/            # Serializers, views, URLs for kan_mind
├── manage.py
└── requirements.txt
```

---

## API Endpoints

> For full endpoint documentation including request/response examples, status
> codes and permissions, see [docs/api.md](docs/api.md).

### Auth

| Method | Endpoint                      | Description                     | Auth required | Access         |
| ------ | ----------------------------- | ------------------------------- | ------------- | -------------- |
| POST   | `/api/registration/`          | Register a new user             | No            | All            |
| POST   | `/api/login/`                 | Log in a user                   | No            | All            |
| GET    | `/api/email-check/?email=...` | Check if a user exists by email | Yes           | Logged-in user |

### Boards

| Method | Endpoint            | Description        | Auth required | Access         |
| ------ | ------------------- | ------------------ | ------------- | -------------- |
| POST   | `/api/boards/`      | Create a board     | Yes           | Logged-in user |
| GET    | `/api/boards/`      | List all boards    | Yes           | Owner, member  |
| GET    | `/api/boards/<id>/` | Retrieve one board | Yes           | Owner, member  |
| PATCH  | `/api/boards/<id>/` | Update a board     | Yes           | Owner, member  |
| DELETE | `/api/boards/<id>/` | Delete a board     | Yes           | Owner only     |

### Tasks

| Method | Endpoint                     | Description               | Auth required | Access                    |
| ------ | ---------------------------- | ------------------------- | ------------- | ------------------------- |
| POST   | `/api/tasks/`                | Create a task             | Yes           | Board member              |
| GET    | `/api/tasks/assigned-to-me/` | List tasks assigned to me | Yes           | Logged-in user            |
| GET    | `/api/tasks/reviewing/`      | List tasks I am reviewing | Yes           | Logged-in user            |
| PATCH  | `/api/tasks/<id>/`           | Update a task             | Yes           | Board member              |
| DELETE | `/api/tasks/<id>/`           | Delete a task             | Yes           | Task creator, board owner |

### Comments

| Method | Endpoint                                     | Description             | Auth required | Access         |
| ------ | -------------------------------------------- | ----------------------- | ------------- | -------------- |
| GET    | `/api/tasks/<id>/comments/`                  | List comments of a task | Yes           | Board member   |
| POST   | `/api/tasks/<id>/comments/`                  | Add a comment to a task | Yes           | Board member   |
| DELETE | `/api/tasks/<task_id>/comments/<comment_id>` | Delete a comment        | Yes           | Comment author |

---

## Frontend

The corresponding frontend repository can be found here:

[Frontend Repository](https://github.com/)

---

## Author

**Philipp Biebert**  
Project status: 07.05.2026
