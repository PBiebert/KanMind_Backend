# KanMind – API Documentation

Base URL: `http://127.0.0.1:8000/api/`  
Authentication: Token-based (`Authorization: Token <your_token>`)

---

## Table of Contents

- [Authentication](#authentication)
  - [POST /registration/](#post-registration)
  - [POST /login/](#post-login)
- [Users](#users)
  - [GET /email-check/](#get-email-check)
- [Boards](#boards)
  - [GET /boards/](#get-boards)
  - [POST /boards/](#post-boards)
  - [GET /boards/{id}/](#get-boardsid)
  - [PATCH /boards/{id}/](#patch-boardsid)
  - [DELETE /boards/{id}/](#delete-boardsid)
- [Tasks](#tasks)
  - [POST /tasks/](#post-tasks)
  - [GET /tasks/assigned-to-me/](#get-tasksassigned-to-me)
  - [GET /tasks/reviewing/](#get-tasksreviewing)
  - [PATCH /tasks/{id}/](#patch-tasksid)
  - [DELETE /tasks/{id}/](#delete-tasksid)
- [Comments](#comments)
  - [GET /tasks/{id}/comments/](#get-tasksidcomments)
  - [POST /tasks/{id}/comments/](#post-tasksidcomments)
  - [DELETE /tasks/{task_id}/comments/{comment_id}/](#delete-taskstask_idcommentscomment_id)

---

## Authentication

### POST /registration/

Registers a new user account.

**Auth required:** No

**Request Body**

```json
{
  "fullname": "Max Mustermann",
  "email": "max.mustermann@example.com",
  "password": "securepassword123",
  "repeated_password": "securepassword123"
}
```

**Success Response `201`**

```json
{
  "token": "abc123...",
  "fullname": "Max Mustermann",
  "email": "max.mustermann@example.com",
  "user_id": 1
}
```

**Status Codes**

| Code | Description                                                        |
| ---- | ------------------------------------------------------------------ |
| 201  | User successfully registered.                                      |
| 400  | Invalid data – e.g. passwords don't match or email already exists. |

---

### POST /login/

Authenticates a user and returns an auth token.

**Auth required:** No

**Request Body**

```json
{
  "email": "max.mustermann@example.com",
  "password": "securepassword123"
}
```

**Success Response `200`**

```json
{
  "token": "abc123...",
  "fullname": "Max Mustermann",
  "email": "max.mustermann@example.com",
  "user_id": 1
}
```

**Status Codes**

| Code | Description          |
| ---- | -------------------- |
| 200  | Login successful.    |
| 400  | Invalid credentials. |

---

## Users

### GET /email-check/

Checks whether a given email address belongs to a registered user.

**Auth required:** Yes  
**Permissions:** Logged-in user

**Query Parameters**

| Name  | Type   | Description                   |
| ----- | ------ | ----------------------------- |
| email | string | The email address to look up. |

**Success Response `200`**

```json
{
  "id": 1,
  "email": "max.mustermann@example.com",
  "fullname": "Max Mustermann"
}
```

**Status Codes**

| Code | Description                            |
| ---- | -------------------------------------- |
| 200  | User found.                            |
| 400  | Missing or malformed email address.    |
| 401  | Unauthorized – user must be logged in. |
| 404  | No user found with this email.         |

---

## Boards

### GET /boards/

Returns all boards the authenticated user is either owner or member of.

**Auth required:** Yes  
**Permissions:** Owner or member of the board

**Success Response `200`**

```json
[
  {
    "id": 1,
    "title": "Project X",
    "member_count": 2,
    "ticket_count": 5,
    "tasks_to_do_count": 2,
    "tasks_high_prio_count": 1,
    "owner_id": 12
  }
]
```

**Status Codes**

| Code | Description                                 |
| ---- | ------------------------------------------- |
| 200  | Success. Returns list of accessible boards. |
| 401  | Unauthorized – user must be logged in.      |

> Only boards the authenticated user has access to are returned.

---

### POST /boards/

Creates a new board. The authenticated user is automatically set as owner.

**Auth required:** Yes  
**Permissions:** Any logged-in user

**Request Body**

```json
{
  "title": "New Project",
  "members": [12, 5, 54, 2]
}
```

**Success Response `200`**

```json
{
  "id": 18,
  "title": "New Project",
  "member_count": 4,
  "ticket_count": 0,
  "tasks_to_do_count": 0,
  "tasks_high_prio_count": 0,
  "owner_id": 2
}
```

**Status Codes**

| Code | Description                                      |
| ---- | ------------------------------------------------ |
| 200  | Board successfully created.                      |
| 400  | Invalid data – e.g. invalid user IDs in members. |
| 401  | Unauthorized – user must be logged in.           |

---

### GET /boards/{id}/

Returns full details of a single board including members and tasks.

**Auth required:** Yes  
**Permissions:** Owner or member of the board

**URL Parameters**

| Name | Type    | Description  |
| ---- | ------- | ------------ |
| id   | integer | The board ID |

**Success Response `200`**

```json
{
  "id": 1,
  "title": "Project X",
  "owner_id": 12,
  "members": [
    {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    }
  ],
  "tasks": [
    {
      "id": 5,
      "title": "Write API docs",
      "description": "Complete the backend API documentation",
      "status": "to-do",
      "priority": "high",
      "assignee": null,
      "reviewer": {
        "id": 1,
        "email": "max.mustermann@example.com",
        "fullname": "Max Mustermann"
      },
      "due_date": "2025-02-25",
      "comments_count": 0
    }
  ]
}
```

**Status Codes**

| Code | Description                              |
| ---- | ---------------------------------------- |
| 200  | Success.                                 |
| 401  | Unauthorized – user must be logged in.   |
| 403  | Forbidden – user is not owner or member. |
| 404  | Board not found.                         |

---

### PATCH /boards/{id}/

Updates the title and/or members of a board. Not intended for updating tasks.

**Auth required:** Yes  
**Permissions:** Owner or member of the board

**URL Parameters**

| Name | Type    | Description  |
| ---- | ------- | ------------ |
| id   | integer | The board ID |

**Request Body**

```json
{
  "title": "Updated Title",
  "members": [1, 54]
}
```

**Success Response `200`**

```json
{
  "id": 3,
  "title": "Updated Title",
  "owner_data": {
    "id": 1,
    "email": "max.mustermann@example.com",
    "fullname": "Max Mustermann"
  },
  "members_data": [
    {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    {
      "id": 54,
      "email": "max.musterfrau@example.com",
      "fullname": "Maxi Musterfrau"
    }
  ]
}
```

**Status Codes**

| Code | Description                              |
| ---- | ---------------------------------------- |
| 200  | Board successfully updated.              |
| 400  | Invalid data.                            |
| 401  | Unauthorized – user must be logged in.   |
| 403  | Forbidden – user is not owner or member. |
| 404  | Board not found.                         |

> Members not included in the request body will be removed from the board.

---

### DELETE /boards/{id}/

Deletes a board permanently. Cascades to all related tasks and comments.

**Auth required:** Yes  
**Permissions:** Owner only

**URL Parameters**

| Name | Type    | Description  |
| ---- | ------- | ------------ |
| id   | integer | The board ID |

**Success Response `204`** – No content

**Status Codes**

| Code | Description                                    |
| ---- | ---------------------------------------------- |
| 204  | Board successfully deleted.                    |
| 401  | Unauthorized – user must be logged in.         |
| 403  | Forbidden – only the owner may delete a board. |
| 404  | Board not found.                               |

> Deleting a board permanently removes all associated tasks and comments.

---

## Tasks

### POST /tasks/

Creates a new task within a board. The authenticated user is set as creator
automatically.

**Auth required:** Yes  
**Permissions:** Board member

**Request Body**

```json
{
  "board": 12,
  "title": "Code Review",
  "description": "Review PR for feature X",
  "status": "review",
  "priority": "medium",
  "assignee_id": 13,
  "reviewer_id": 1,
  "due_date": "2025-02-27"
}
```

Valid values for `status`: `to-do` · `in-progress` · `review` · `done`  
Valid values for `priority`: `low` · `medium` · `high`

**Success Response `201`**

```json
{
  "id": 10,
  "board": 12,
  "title": "Code Review",
  "description": "Review PR for feature X",
  "status": "review",
  "priority": "medium",
  "assignee": {
    "id": 13,
    "email": "marie@example.com",
    "fullname": "Marie Musterfrau"
  },
  "reviewer": {
    "id": 1,
    "email": "max@example.com",
    "fullname": "Max Mustermann"
  },
  "due_date": "2025-02-27",
  "comments_count": 0
}
```

**Status Codes**

| Code | Description                               |
| ---- | ----------------------------------------- |
| 201  | Task successfully created.                |
| 400  | Invalid data – missing or invalid fields. |
| 401  | Unauthorized – user must be logged in.    |
| 403  | Forbidden – user is not a board member.   |
| 404  | Board not found.                          |

> `assignee` and `reviewer` must be members of the board. Both fields are
> optional.

---

### GET /tasks/assigned-to-me/

Returns all tasks where the authenticated user is set as assignee.

**Auth required:** Yes  
**Permissions:** Logged-in user

**Success Response `200`**

```json
[
  {
    "id": 1,
    "board": 1,
    "title": "Task 1",
    "description": "...",
    "status": "to-do",
    "priority": "high",
    "assignee": {
      "id": 13,
      "email": "marie@example.com",
      "fullname": "Marie Musterfrau"
    },
    "reviewer": {
      "id": 1,
      "email": "max@example.com",
      "fullname": "Max Mustermann"
    },
    "due_date": "2025-02-25",
    "comments_count": 0
  }
]
```

**Status Codes**

| Code | Description                            |
| ---- | -------------------------------------- |
| 200  | Success.                               |
| 401  | Unauthorized – user must be logged in. |

---

### GET /tasks/reviewing/

Returns all tasks where the authenticated user is set as reviewer.

**Auth required:** Yes  
**Permissions:** Logged-in user

**Success Response `200`**  
Same structure as [`GET /tasks/assigned-to-me/`](#get-tasksassigned-to-me).

**Status Codes**

| Code | Description                            |
| ---- | -------------------------------------- |
| 200  | Success.                               |
| 401  | Unauthorized – user must be logged in. |

---

### PATCH /tasks/{id}/

Partially updates an existing task. Changing the board field is not allowed.

**Auth required:** Yes  
**Permissions:** Board member

**URL Parameters**

| Name | Type    | Description |
| ---- | ------- | ----------- |
| id   | integer | The task ID |

**Request Body** _(all fields optional)_

```json
{
  "title": "Finish Code Review",
  "description": "Review the PR and leave feedback",
  "status": "done",
  "priority": "high",
  "assignee_id": 13,
  "reviewer_id": 1,
  "due_date": "2025-02-28"
}
```

**Success Response `200`**

```json
{
  "id": 10,
  "title": "Finish Code Review",
  "description": "Review the PR and leave feedback",
  "status": "done",
  "priority": "high",
  "assignee": {
    "id": 13,
    "email": "marie@example.com",
    "fullname": "Marie Musterfrau"
  },
  "reviewer": {
    "id": 1,
    "email": "max@example.com",
    "fullname": "Max Mustermann"
  },
  "due_date": "2025-02-28",
  "comments_count": 2
}
```

**Status Codes**

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | Task successfully updated.              |
| 400  | Invalid data.                           |
| 401  | Unauthorized – user must be logged in.  |
| 403  | Forbidden – user is not a board member. |
| 404  | Task not found.                         |

---

### DELETE /tasks/{id}/

Deletes a task. Only the task creator or board owner may delete it.

**Auth required:** Yes  
**Permissions:** Task creator or board owner

**URL Parameters**

| Name | Type    | Description |
| ---- | ------- | ----------- |
| id   | integer | The task ID |

**Success Response `204`** – No content

**Status Codes**

| Code | Description                                              |
| ---- | -------------------------------------------------------- |
| 204  | Task successfully deleted.                               |
| 401  | Unauthorized – user must be logged in.                   |
| 403  | Forbidden – user is not the task creator or board owner. |
| 404  | Task not found.                                          |

> Deletion is permanent and cannot be undone.

---

## Comments

### GET /tasks/{id}/comments/

Returns all comments for a specific task.

**Auth required:** Yes  
**Permissions:** Board member

**URL Parameters**

| Name | Type    | Description |
| ---- | ------- | ----------- |
| id   | integer | The task ID |

**Success Response `200`**

```json
[
  {
    "id": 1,
    "created_at": "2025-02-20T14:30:00Z",
    "author": "Max Mustermann",
    "content": "This is a comment on the task."
  },
  {
    "id": 2,
    "created_at": "2025-02-21T09:15:00Z",
    "author": "Erika Musterfrau",
    "content": "Another comment for the discussion."
  }
]
```

**Status Codes**

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | Success.                                |
| 401  | Unauthorized – user must be logged in.  |
| 403  | Forbidden – user is not a board member. |
| 404  | Task not found.                         |

---

### POST /tasks/{id}/comments/

Adds a new comment to a task. The author is determined automatically from the
auth token.

**Auth required:** Yes  
**Permissions:** Board member

**URL Parameters**

| Name | Type    | Description |
| ---- | ------- | ----------- |
| id   | integer | The task ID |

**Request Body**

```json
{
  "content": "This is a new comment."
}
```

**Success Response `200`**

```json
{
  "id": 15,
  "created_at": "2025-02-20T15:00:00Z",
  "author": "Max Mustermann",
  "content": "This is a new comment."
}
```

**Status Codes**

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | Comment successfully created.           |
| 400  | Invalid data – e.g. empty content.      |
| 401  | Unauthorized – user must be logged in.  |
| 403  | Forbidden – user is not a board member. |
| 404  | Task not found.                         |

---

### DELETE /tasks/{task_id}/comments/{comment_id}/

Deletes a comment. Only the comment author may delete it.

**Auth required:** Yes  
**Permissions:** Comment author

**URL Parameters**

| Name       | Type    | Description    |
| ---------- | ------- | -------------- |
| task_id    | integer | The task ID    |
| comment_id | integer | The comment ID |

**Success Response `204`** – No content

**Status Codes**

| Code | Description                                 |
| ---- | ------------------------------------------- |
| 204  | Comment successfully deleted.               |
| 401  | Unauthorized – user must be logged in.      |
| 403  | Forbidden – user is not the comment author. |
| 404  | Task or comment not found.                  |
