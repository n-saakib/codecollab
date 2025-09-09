from django.urls import path
from django.views.generic import RedirectView

from projects.views import ProjectDashboardView

urlpatterns=[
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=True)),
    path('dashboard/', ProjectDashboardView.as_view(), name='dashboard'),
]