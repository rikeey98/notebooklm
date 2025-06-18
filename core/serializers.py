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
    notebook = serializers.IntegerField(write_only=True)
    tag = serializers.ListField(child=serializers.CharField(), write_only=True, required=False, default=list)
    content = serializers.CharField(write_only=True)
    link = serializers.URLField(write_only=True, required=False, allow_null=True, default=None)

    class Meta:
        model = Source
        fields = '__all__'
        extra_fields = ['notebook', 'tag', 'content', 'link']

    def create(self, validated_data):
        notebook_id = validated_data.pop('notebook')
        tag = validated_data.pop('tag')
        content = validated_data.pop('content')
        link = validated_data.pop('link', None)
        source = super().create(validated_data)
        from .models import SourceMetadata, Notebook, NotebookMap
        SourceMetadata.objects.create(
            source=source,
            title=source.title,
            tag=tag,
            content=content,
            link=link
        )
        # NotebookMap 생성
        notebook = Notebook.objects.get(id=notebook_id)
        NotebookMap.objects.create(notebook=notebook, source=source)
        return source

class SourceDetailSerializer(serializers.ModelSerializer):
    metadata = serializers.SerializerMethodField(read_only=True)
    summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Source
        fields = '__all__'
        extra_fields = ['metadata', 'summary']

    def get_metadata(self, obj):
        from .serializers import SourceMetadataSerializer
        if hasattr(obj, 'sourcemetadata'):
            return SourceMetadataSerializer(obj.sourcemetadata).data
        return None

    def get_summary(self, obj):
        from .serializers import SourceSummarySerializer
        if hasattr(obj, 'sourcesummary'):
            return SourceSummarySerializer(obj.sourcesummary).data
        return None

class NotebookMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookMap
        fields = '__all__'

class SourceMetadataSerializer(serializers.ModelSerializer):
    link = serializers.URLField(required=False, allow_null=True, default=None)
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