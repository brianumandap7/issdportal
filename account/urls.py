
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthForm

urlpatterns = [
    
    path('users/register', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user = True, authentication_form=CustomAuthForm), name = 'login'),
    path('users/logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('profile/', views.profile, name='profile'),

    # JASB STARTS
    path('account/employeemanagement', views.employee_management, name='employee-mgt'),
    path('account/modalemployee', views.employee_modal, name='modal-employee'),
    path('account/createmployee', views.employee_create, name='create-employee'),
    path('account/listemployee', views.employee_list, name='list-employee'),
    # JASB ENDS

    

]