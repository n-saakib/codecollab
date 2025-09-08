from django.contrib import admin

from projects.models import ProjectMembership, Project, Folder, File


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    """
    Admin view for the through model ProjectMembership.
    Useful for seeing a full list of all memberships across all projects.
    """
    list_display = ('project', 'member', 'role')
    list_filter = ('role', 'project', 'member')
    search_fields = ('project__name', 'member__username')
    autocomplete_fields = ('project', 'member')


class ProjectMembershipInline(admin.TabularInline):
    """
    This class tells the admin: 'When I'm looking at a Project,
    let me edit the members directly on the same page.'
    It provides a more compact, table-like layout for the members.
    """
    model = ProjectMembership
    autocomplete_fields = ('member', 'project')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    This class customizes how the Project list and edit pages look and behave.
    """
    list_display = ['name', 'owner', 'created_at']
    search_fields = ['name', 'owner__username']
    autocomplete_fields = ['owner']
    inlines = [ProjectMembershipInline]


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """ Customizes the admin for the Folder model. """
    list_display = ['name', 'project', 'parent']
    search_fields = ['name', 'project__name', 'parent__name']
    autocomplete_fields = ('project', 'parent')
    list_filter = ['project']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """ Customizes the admin for the File model. """
    list_display = ['name', 'project', 'parent', 'language', 'updated_at']
    search_fields = ['name', 'project__name', 'parent__name', 'language']
    autocomplete_fields = ('project', 'parent')
    list_filter = ['project', 'language']
