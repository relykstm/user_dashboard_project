from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register_page),
    path('signin', views.sign_in_page),
    path('register_new_user', views.register),
    path('login_user', views.login_check),
    path('logout', views.logout),
    path('dashboard/admin', views.admin_dashboard),
    path('dashboard', views.normal_dashboard),
    path('users/edit', views.edit_own_profile),
    path('dashboardroute', views.which_dashboard),
    path('users/edit/<id>', views.edit_a_profile),
    path('users/show/<id>', views.show_a_profile),
    path('users/new', views.create_new_user_page),
    path('users/admin_create_user', views.admin_create_user),
    path('users/delete/<id>', views.delete_user), 
    path('users/updatepassword/<id>', views.update_password),
    path('edituserinfo/<id>', views.edit_user_info),
    path('updatemydescription', views.update_my_description),
    path('updateinformation', views.update_my_info),
    path('submitpost', views.add_new_post),
    path('submitcomment', views.add_new_comment)
] 