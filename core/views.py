from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import *
from .serializers import *
from django.contrib.auth.models import User

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
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

    def get_queryset(self):
        queryset = JiraConfig.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

class MailConfigViewSet(viewsets.ModelViewSet):
    queryset = MailConfig.objects.all()
    serializer_class = MailConfigSerializer

    def get_queryset(self):
        queryset = MailConfig.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
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
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            from .serializers import SourceDetailSerializer
            return SourceDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Source.objects.all()
        user_id = self.request.query_params.get('user_id')
        project_id = self.request.query_params.get('project')
        notebook_id = self.request.query_params.get('notebook')
        title = self.request.query_params.get('title')
        if user_id is not None:
            queryset = queryset.filter(create_user_id=user_id)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        if notebook_id is not None:
            from .models import NotebookMap
            source_ids = NotebookMap.objects.filter(notebook_id=notebook_id).values_list('source_id', flat=True)
            queryset = queryset.filter(id__in=source_ids)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

class NotebookMapViewSet(viewsets.ModelViewSet):
    queryset = NotebookMap.objects.all()
    serializer_class = NotebookMapSerializer

class SourceMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SourceMetadata.objects.all()
    serializer_class = SourceMetadataSerializer

class SourceSummaryViewSet(viewsets.ModelViewSet):
    queryset = SourceSummary.objects.all()
    serializer_class = SourceSummarySerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
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

# NotebookViewSet 등은 name 필드 자동 반영됨. name으로 필터링 원하면 아래와 같이 추가 가능:
# name = self.request.query_params.get('name')
# if name is not None:
#     queryset = queryset.filter(name__icontains=name)
