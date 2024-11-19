from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
