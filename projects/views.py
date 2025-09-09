from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets, permissions

from projects.forms import ProjectForm
from projects.models import Project, Folder, File
from projects.permissions import IsProjectMember
from projects.serializers import ProjectSerializer, FolderSerializer, FileSerializer


class ProjectDashboardView(LoginRequiredMixin, generic.ListView):
    """
    This view displays a list of projects that the currently logged-in
    user is a member of.
    """
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


class ProjectEditorView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/editor.html'

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        self.object.members.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse('editor', kwargs={'pk': self.object.pk})


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectMember)

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


class FolderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Folders to be viewed or edited.
    """
    serializer_class = FolderSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectMember)

    def get_queryset(self):
        return Folder.objects.filter(project__members=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Files to be viewed or edited.
    """
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectMember)

    def get_queryset(self):
        return File.objects.filter(project__members=self.request.user)