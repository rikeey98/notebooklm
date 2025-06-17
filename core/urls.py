from rest_framework import routers
from .views import *

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

urlpatterns = router.urls 