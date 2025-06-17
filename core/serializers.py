from rest_framework import serializers
from .models import (
    Project, JiraConfig, MailConfig, Notebook, Source,
    NotebookMap, SourceMetadata, SourceSummary, Output
)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class JiraConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraConfig
        fields = '__all__'

class MailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailConfig
        fields = '__all__'

class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = '__all__'

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class NotebookMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookMap
        fields = '__all__'

class SourceMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceMetadata
        fields = '__all__'

class SourceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceSummary
        fields = '__all__'

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = '__all__' 