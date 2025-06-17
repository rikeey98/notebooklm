from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import *
from .serializers import *
from django.contrib.auth.models import User

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class JiraConfigViewSet(viewsets.ModelViewSet):
    queryset = JiraConfig.objects.all()
    serializer_class = JiraConfigSerializer

class MailConfigViewSet(viewsets.ModelViewSet):
    queryset = MailConfig.objects.all()
    serializer_class = MailConfigSerializer

class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer

    def get_queryset(self):
        queryset = Notebook.objects.all()
        user_id = self.request.query_params.get('user_id')
        project_id = self.request.query_params.get('project_id')
        if user_id is not None:
            queryset = queryset.filter(create_user_id=user_id)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer

    def get_queryset(self):
        queryset = Source.objects.all()
        user_id = self.request.query_params.get('user_id')
        project_id = self.request.query_params.get('project')
        notebook_id = self.request.query_params.get('notebook')
        if user_id is not None:
            queryset = queryset.filter(create_user_id=user_id)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        if notebook_id is not None:
            from .models import NotebookMap
            source_ids = NotebookMap.objects.filter(notebook_id=notebook_id).values_list('source_id', flat=True)
            queryset = queryset.filter(id__in=source_ids)
        return queryset

class NotebookMapViewSet(viewsets.ModelViewSet):
    queryset = NotebookMap.objects.all()
    serializer_class = NotebookMapSerializer

class SourceMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SourceMetadata.objects.all()
    serializer_class = SourceMetadataSerializer

class SourceSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SourceSummary.objects.all()
    serializer_class = SourceSummarySerializer

class OutputViewSet(viewsets.ModelViewSet):
    serializer_class = OutputSerializer

    def get_queryset(self):
        queryset = Output.objects.all()
        user_id = self.request.query_params.get('user')
        project_id = self.request.query_params.get('project')
        notebook_id = self.request.query_params.get('notebook')
        if user_id is not None:
            queryset = queryset.filter(create_user_id=user_id)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        if notebook_id is not None:
            queryset = queryset.filter(notebook_id=notebook_id)
        return queryset

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
