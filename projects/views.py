from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.forms import ProjectForm
from projects.models import Project, Folder, File
from projects.permissions import IsProjectMember, IsProjectOwner
from projects.serializers import ProjectSerializer, FolderSerializer, FileSerializer
from users.models import User


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

    @action(detail=True, methods=['post'], permission_classes=[IsProjectOwner])
    def add_member(self, request, pk=None):
        """
        Custom action to add a new member to a project.
        Expects a POST request with a 'username' in the body.
        """
        project = self.get_object()
        username = request.data.get('username')

        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_add = User.objects.get(username=username)
            if user_to_add in project.members.all():
                return Response({'error': 'User is already a member.'}, status=status.HTTP_400_BAD_REQUEST)

            project.members.add(user_to_add)
            return Response({'success': f"User '{username}' added successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


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