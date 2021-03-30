from .serlializers import ProjectSerializer, CategorySerializer
from .models import ProjectTags, Project, Category
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class TagTitleFilter(generics.ListAPIView):
    queryset = ProjectTags.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['project__title', 'tag']


class CategoryFilter(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__title']
