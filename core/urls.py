from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'jira-configs', JiraConfigViewSet)
router.register(r'mail-configs', MailConfigViewSet)
router.register(r'notebooks', NotebookViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'notebook-maps', NotebookMapViewSet)
router.register(r'source-metadata', SourceMetadataViewSet)
router.register(r'source-summary', SourceSummaryViewSet)
router.register(r'outputs', OutputViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls + [
    path('source-bulk-delete/', BulkDeleteSourceView.as_view(), name='bulk-delete-source'),
    path('send-mail/', SendMailView.as_view(), name='send-mail'),
] 