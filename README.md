## Features

- **Project Management**: Create, update, delete, and list projects
- **Task Management**: Full CRUD operations with status tracking
- **User Assignment**: Assign tasks to users with email notifications
- **Activity Logging**: Automatic logging when tasks are created
- **Advanced Filtering**: Filter tasks by status, assignee, and due date
- **Custom Actions**: Mark tasks as complete, view overdue tasks
- **Authentication**: JWT-based authentication
- **Permissions**: Role-based access control (project owners and task assignees)

## Requirements

- Python 3.12+
- Django 6.0+
- Django REST Framework 3.14+
- django-filter 23.0+
- djangorestframework-simplejwt 5.3+

## Installation

1. **Clone the repository and navigate to the project directory**

2. **Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd task_management
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Start the development server**
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /auth/login/` - Get JWT access and refresh tokens
- `POST /auth/refresh/` - Refresh access token

### Projects
- `GET /api/projects/` - List all projects (paginated, searchable)
- `POST /api/projects/` - Create a new project (with optional nested tasks)
- `GET /api/projects/{id}/` - Retrieve project details
- `PUT/PATCH /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Tasks
- `GET /api/tasks/` - List all tasks (filterable, searchable, paginated)
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Retrieve task details
- `PUT/PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/mark_complete/` - Mark task as completed
- `GET /api/tasks/overdue/` - List overdue tasks

## API Usage Examples

### 1. Login
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

### 2. Create Project with Tasks
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description",
    "create_tasks": [
      {
        "title": "Task 1",
        "description": "Task description",
        "due_date": "2026-12-31",
        "assigned_to": 1,
        "status": "todo"
      }
    ]
  }'
```

### 3. List Tasks with Filters
```bash
# Filter by status
curl -X GET "http://localhost:8000/api/tasks/?status=completed" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by assignee
curl -X GET "http://localhost:8000/api/tasks/?assigned_to=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Search by title
curl -X GET "http://localhost:8000/api/tasks/?search=important" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Mark Task as Complete
```bash
curl -X POST http://localhost:8000/api/tasks/1/mark_complete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Overdue Tasks
```bash
curl -X GET http://localhost:8000/api/tasks/overdue/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
task_management/
├── core/                          # Main application
│   ├── models.py                  # Project, Task, TaskActivityLog models
│   ├── serializers.py             # API serializers with validation
│   ├── views.py                   # ViewSets with filtering & permissions
│   ├── permissions.py             # Custom permission classes
│   ├── signals.py                 # Post-save signal handlers
│   ├── urls.py                    # API routing
│   └── apps.py                    # App configuration
├── task_management/               # Project settings
│   ├── settings.py                # Django settings
│   └── urls.py                    # Root URL configuration
├── logs/                          # Application logs
│   ├── tasks.log                  # Task creation logs
│   └── errors.log                 # Error logs
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
```

## Models

### Project
- `name`: Project name
- `description`: Project description
- `owner`: User who owns the project
- `created_at`: Timestamp of creation

### Task
- `project`: Foreign key to Project
- `title`: Task title
- `description`: Task description
- `status`: One of: todo, in_progress, completed
- `due_date`: Task due date
- `assigned_to`: User assigned to the task
- `created_at`: Timestamp of creation

### TaskActivityLog
- `task`: Foreign key to Task
- `message`: Activity log message
- `created_at`: Timestamp of log entry

## Permissions

### Project Permissions
- Only the project owner can update or delete a project
- Users can only see their own projects

### Task Permissions
- Task can be modified by:
  - The assigned user, OR
  - The project owner
- Users can see tasks from:
  - Projects they own, OR
  - Tasks assigned to them

## Features

### Validation
- Due dates cannot be in the past
- Description is required when marking a task as completed
- Proper error messages for validation failures

### Activity Logging
- Automatic activity log creation when tasks are created
- Optional email notification when tasks are assigned
- File logging for audit trails

### Transaction Safety
- Creating a project with nested tasks uses atomic transactions
- If any task fails validation, the entire operation rolls back

## Configuration

### Email Settings
By default, emails are printed to console. To configure SMTP:


## Development

### Running the Server
```bash
python manage.py runserver
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
