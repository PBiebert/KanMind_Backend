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
   python -m venv env
   source env/bin/activate        # Mac/Linux
   env\Scripts\activate           # Windows
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

| Method | Endpoint                      | Description                    | Auth required | Access         |
| ------ | ----------------------------- | ------------------------------ | ------------- | -------------- |
| POST   | `/api/registration/`          | Register a new user            | No            | all            |
| POST   | `/api/login/`                 | Log in a user                  | No            | all            |
| GET    | `/api/email-check/?email=...` | Check if user exists by E-Mail | Yes           | Logged-in user |
| POST   | `/api/boards/`                | Create a board                 | Yes           | owner          |
| GET    | `/api/boards/`                | Retrieve all boards            | Yes           | owner, member  |
| GET    | `/api/boards/<int:pk>/`       | Retrieve one board             | Yes           | owner, member  |
| PATCH  | `/api/boards/<int:pk>/`       | Update a board                 | Yes           | owner, member  |
| DELETE | `/api/boards/<int:pk>/`       | Delete a board                 | Yes           | owner          |

---

## Frontend

The corresponding frontend repository can be found here:

> [Link to be added]

---

## Author

**Philipp Biebert**  
Project status: 07.05.2026
