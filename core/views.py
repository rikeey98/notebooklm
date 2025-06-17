from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import *
from .serializers import *
from django.contrib.auth.models import User

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class JiraConfigViewSet(viewsets.ModelViewSet):
    queryset = JiraConfig.objects.all()
    serializer_class = JiraConfigSerializer

class MailConfigViewSet(viewsets.ModelViewSet):
    queryset = MailConfig.objects.all()
    serializer_class = MailConfigSerializer

class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class NotebookMapViewSet(viewsets.ModelViewSet):
    queryset = NotebookMap.objects.all()
    serializer_class = NotebookMapSerializer

class SourceMetadataViewSet(viewsets.ModelViewSet):
    queryset = SourceMetadata.objects.all()
    serializer_class = SourceMetadataSerializer

class SourceSummaryViewSet(viewsets.ModelViewSet):
    queryset = SourceSummary.objects.all()
    serializer_class = SourceSummarySerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
