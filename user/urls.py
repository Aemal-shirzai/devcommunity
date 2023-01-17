from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='profile_index'),
    path('login/', views.login_user, name='profile_login'),
    path('logout/', views.logout_user, name='profile_logout'),
    path('register/', views.register_user, name='profile_register'),
    path('account/', views.account, name='profile_account'),
    path('account/edit', views.account_edit, name='profile_account_edit'),
    path('account/skills', views.account_skills_create, name='profile_account_skills_create'),
    path('account/skills/edit/<int:id>', views.account_skills_edit, name='profile_account_skills_edit'),
    path('account/skills/delete/<int:id>', views.account_skills_delete, name='profile_account_skills_delete'),
    path('account/inbox', views.account_inbox, name='account_inbox'),
    path('<int:id>', views.show, name='profile_show')
]