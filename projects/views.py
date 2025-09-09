from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from projects.models import Project


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