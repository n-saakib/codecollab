from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignupForm(UserCreationForm):
    """
    A custom form for user registration that inherits from Django's
    built-in UserCreationForm.
    """
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')