from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from project.models import Project
from .serializer import ProjectSerializer


@api_view()
def get_projects(request):
    projects = Project.objects.all()
    serialized_projects = ProjectSerializer(projects, many=True)
    return Response(serialized_projects.data, status=status.HTTP_200_OK)


@api_view()
def get_project(request, id):
    try:
        projects = Project.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_projects = ProjectSerializer(projects)
    return Response(serialized_projects.data, status=status.HTTP_200_OK)