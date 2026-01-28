from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (TODO, "Todo"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=TODO
    )
    due_date = models.DateField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskActivityLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activities")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)