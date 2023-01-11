from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='profile_index'),
    path('login/', views.login_user, name='profile_login'),
    path('logout/', views.logout_user, name='profile_logout'),
    path('<int:id>', views.show, name='profile_show')
]