from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User

# List, Create, Retrieve, Update, Delete Clients
class ClientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client)
        else:
            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# List, Create, Retrieve, Delete Projects
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ProjectSerializer
from django.contrib.auth.models import User

class ProjectView(APIView):
    def post(self, request):
        data = request.data
        print("Received data:", data)  # Debug statement
        client_id = data.get('client_id')
        print("Client ID:", client_id)  # Debug statement

        # Check if client_id is not None and is valid
        if not client_id:
            return Response({"error": "Client ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            print("Client does not exist")  # Debug statement
            return Response({"error": "Client does not exist."}, status=status.HTTP_404_NOT_FOUND)

        project = Project.objects.create(
            project_name=data['project_name'],
            client=client,
            created_by=request.user
        )
        users = User.objects.filter(id__in=data['users'])
        project.users.set(users)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

