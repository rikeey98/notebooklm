from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

class JiraConfig(models.Model):
    url = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class MailConfig(models.Model):
    recipients = models.TextField()  # 콤마로 구분된 이메일 리스트 등
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Notebook(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class Source(models.Model):
    title = models.CharField(max_length=200, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

class NotebookMap(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

class SourceMetadata(models.Model):
    source = models.OneToOneField(Source, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    tag = models.JSONField(default=list)  # 태그 리스트
    content = models.TextField()

class SourceSummary(models.Model):
    source = models.OneToOneField(Source, on_delete=models.CASCADE, primary_key=True)
    summary = models.TextField()

class Output(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
