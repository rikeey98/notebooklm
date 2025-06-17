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
    metadata = serializers.SerializerMethodField(read_only=True)
    summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Source
        fields = '__all__'
        extra_fields = ['metadata', 'summary']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['metadata'] = self.get_metadata(instance)
        rep['summary'] = self.get_summary(instance)
        return rep

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

    def create(self, validated_data):
        source = super().create(validated_data)
        # SourceMetadata와 SourceSummary 자동 생성
        from .models import SourceMetadata, SourceSummary
        SourceMetadata.objects.create(
            source=source,
            title=source.title,
            tag=[],
            content=''
        )
        SourceSummary.objects.create(
            source=source,
            summary=''
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