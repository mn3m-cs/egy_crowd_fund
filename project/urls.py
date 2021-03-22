from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_project/', views.ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_details'),
    
]
