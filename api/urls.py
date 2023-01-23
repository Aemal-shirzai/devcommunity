from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('projects', views.get_projects, name='api_get_projects'),
  path('projects/<int:id>', views.get_project, name='api_get_project'),
  path('projects/<int:id>/vote', views.vote_project, name='api_vote_project')
]