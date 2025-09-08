from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models


# This helps mypy and other type checkers understand the User type
# without causing a circular import error.
if TYPE_CHECKING:
    from users.models import User

class Project(models.Model):
    """
    Represents a collaborative workspace containing files and folders.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        through='ProjectMembership'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_members(self):
        return list(self.members.all())

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    """
    Acts as a "through" model to define the relationship between
    a User and a Project, specifying their role.
    """
    class Role(models.TextChoices):
        EDITOR = 'EDITOR', 'Editor'
        VIEWER = 'VIEWER', 'Viewer'

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices, max_length=10, default=Role.EDITOR)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.project.name} as {self.get_role_display()}"


class FileSystemItem(models.Model):
    """
    An abstract base class for Files and Folders to share common fields.
    """
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='%(class)s_items'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
        unique_together = ('project', 'parent', 'name')

    def __str__(self):
        return self.name


class Folder(FileSystemItem):
    """
    Represents a folder in the project's file system.
    """
    pass


class File(FileSystemItem):
    """
    Represents a code file in the project's file system.
    """
    content: models.TextField = models.TextField(blank=True, default='')
    language: models.CharField = models.CharField(
        max_length=50,
        blank=True,
        default='plaintext'
    )