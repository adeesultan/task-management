from django.db import transaction
from django.utils.timezone import now
from rest_framework import serializers

from .models import Project, Task, TaskActivityLog
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate_due_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, attrs):
        status = attrs.get("status")
        description = attrs.get("description")

        if status == Task.COMPLETED and not description:
            raise serializers.ValidationError(
                "Description is required to mark task as completed."
            )

        assigned_to = attrs.get("assigned_to")
        project = attrs.get("project")

        # Note: Organization validation removed as User model doesn't have organization field
        # If organization support is needed, add it to the User model first

        return attrs


class ProjectTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("project",)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    create_tasks = ProjectTaskCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "created_at",
            "tasks",
            "create_tasks",
        )
        read_only_fields = ("created_at", "owner")

    def create(self, validated_data):
        tasks_data = validated_data.pop("create_tasks", [])

        with transaction.atomic():
            project = Project.objects.create(**validated_data)

            for task_data in tasks_data:
                Task.objects.create(project=project, **task_data)

        return project



