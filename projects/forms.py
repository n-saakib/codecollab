from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    """
    A form for creating a new Project instance.
    """
    class Meta:
        model = Project
        fields = ['title', 'description']