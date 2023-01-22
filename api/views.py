from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from project.models import Project, Review
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
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vote_project(request, id):
    data = request.data
    profile = request.user.profile
    try:
        project = Project.objects.get(id=id)
    except:
        return Response({"response": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if not data.get("value") or not data.get("value").lower() in ['up', 'down']:
        return Response({"response": "value should be present in request with up or down values only."}, status=status.HTTP_501_NOT_IMPLEMENTED)

    review, created = Review.objects.get_or_create(owner=profile, project=project)
    review.value = data.get('value')  
    review.save()

    serialized_project = ProjectSerializer(project)
    return Response(serialized_project.data, status=status.HTTP_200_OK)