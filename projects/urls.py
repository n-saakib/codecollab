from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from projects.views import ProjectDashboardView, ProjectViewSet, FileViewSet, FolderViewSet, ProjectEditorView, \
    ProjectCreateView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'files', FileViewSet, basename='file')

urlpatterns=[
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=True)),
    path('dashboard/', ProjectDashboardView.as_view(), name='dashboard'),
    path('api/', include(router.urls)),
    path('projects/<int:pk>/', ProjectEditorView.as_view(), name='editor'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
]