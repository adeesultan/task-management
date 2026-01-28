from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsProjectOwner, IsTaskEditor


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskEditor]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ["status", "assigned_to", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        # Show tasks from projects owned by the user, or tasks assigned to the user
        return Task.objects.filter(
            Q(project__owner=self.request.user) | 
            Q(assigned_to=self.request.user)
        )

    @action(detail=True, methods=["post"])
    def mark_complete(self, request, pk=None):
        task = self.get_object()

        serializer = self.get_serializer(
            task,
            data={"status": Task.COMPLETED},
            partial=True
        )
        
        # Validate explicitly without raise_exception for proper control flow
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Task marked as completed."})
        
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        queryset = self.get_queryset().filter(
            due_date__lt=now().date(),
            status__in=[Task.TODO, Task.IN_PROGRESS]
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)