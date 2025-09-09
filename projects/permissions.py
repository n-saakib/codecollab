from rest_framework import permissions

from projects.models import Project


class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow members of a project to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        project: Project | None = None

        if isinstance(obj, Project):
            project = obj
        else:
            project = obj.project

        return project is not None and project.members.filter(id=request.user.id).exists()