from django.urls import path
from .views import ClientView, ProjectView

urlpatterns = [
    path('', ClientView.as_view()),
    path('clients/', ClientView.as_view()),
    path('clients/<int:pk>/', ClientView.as_view()),
    path('projects/', ProjectView.as_view()),
    path('projects/<int:pk>/', ProjectView.as_view()),
]
