from rest_framework import serializers
from .models import Project, Folder, File
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """ A serializer for our custom User model, showing basic info. """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class FileSerializer(serializers.ModelSerializer):
    """ A serializer for the File model. """
    class Meta:
        model = File
        fields = ['id', 'name', 'language', 'content', 'project', 'parent', 'created_at', 'last_modified']
        read_only_fields = ['created_at', 'last_modified']


class FolderSerializer(serializers.ModelSerializer):
    """ A serializer for the Folder model. """
    class Meta:
        model = Folder
        fields = ['id', 'name', 'project', 'parent', 'created_at', 'last_modified']
        read_only_fields = ['created_at', 'last_modified']


class ProjectSerializer(serializers.ModelSerializer):
    """ A serializer for the Project model. """
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at']
        read_only_fields = ['created_at']
