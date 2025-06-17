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
    metadata = serializers.DictField(write_only=True)
    summary = serializers.CharField(write_only=True)
    metadata_detail = serializers.SerializerMethodField(read_only=True)
    summary_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Source
        fields = '__all__'
        extra_fields = ['metadata', 'summary', 'metadata_detail', 'summary_detail']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['metadata'] = self.get_metadata_detail(instance)
        rep['summary'] = self.get_summary_detail(instance)
        return rep

    def get_metadata_detail(self, obj):
        from .serializers import SourceMetadataSerializer
        if hasattr(obj, 'sourcemetadata'):
            return SourceMetadataSerializer(obj.sourcemetadata).data
        return None

    def get_summary_detail(self, obj):
        from .serializers import SourceSummarySerializer
        if hasattr(obj, 'sourcesummary'):
            return SourceSummarySerializer(obj.sourcesummary).data
        return None

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        summary_data = validated_data.pop('summary')
        source = super().create(validated_data)
        from .models import SourceMetadata, SourceSummary
        SourceMetadata.objects.create(
            source=source,
            title=source.title,
            tag=metadata_data.get('tag', []),
            content=metadata_data.get('content', '')
        )
        SourceSummary.objects.create(
            source=source,
            summary=summary_data
        )
        return source

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