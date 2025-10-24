from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import cs

urlpatterns = [
    path('', login_required(views.cs), name='cs'),
]

