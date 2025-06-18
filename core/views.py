from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .oracle_service import insert_data_to_oracle
from rest_framework.decorators import api_view
from django.db import transaction
from .mail_send_service import save_mail_to_mongodb

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

class BulkDeleteSourceView(APIView):
    def delete(self, request):
        project_id = request.query_params.get('project_id')
        notebook_id = request.query_params.get('notebook_id')
        user_id = request.query_params.get('user_id')
        params = [p for p in [project_id, notebook_id, user_id] if p is not None]
        if len(params) == 0:
            return Response({'error': 'project_id, notebook_id, user_id 중 하나는 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(params) > 1:
            return Response({'error': '한 번에 하나의 파라미터만 허용됩니다.'}, status=status.HTTP_400_BAD_REQUEST)
        count = 0
        with transaction.atomic():
            if project_id is not None:
                count, _ = Source.objects.filter(project_id=project_id).delete()
            elif notebook_id is not None:
                from .models import NotebookMap
                source_ids = NotebookMap.objects.filter(notebook_id=notebook_id).values_list('source_id', flat=True)
                count, _ = Source.objects.filter(id__in=source_ids).delete()
            elif user_id is not None:
                count, _ = Source.objects.filter(create_user_id=user_id).delete()
        return Response({'deleted': count}, status=status.HTTP_200_OK)

class SendMailView(APIView):
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        recipients = request.data.get('recipients')
        if not title or not content or not recipients:
            return Response({'error': 'title, content, recipients는 모두 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            inserted_id = save_mail_to_mongodb(title, content, recipients)
            return Response({'result': 'success', 'id': inserted_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
