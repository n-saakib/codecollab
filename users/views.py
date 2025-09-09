from django.urls import reverse_lazy
from django.views import generic

from users.forms import SignupForm


class SignupView(generic.CreateView):
    """
    A class-based view that handles the user registration process.
    """
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class LoginView():
    pass
