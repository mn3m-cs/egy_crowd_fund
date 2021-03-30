from rest_framework import serializers
from .models import ProjectTags, Category, Project


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='project.title')
    category = serializers.CharField(source='project.category')
    details = serializers.CharField(source='project.details')
    start_time = serializers.CharField(source='project.start_time')
    end_time = serializers.CharField(source='project.end_time')
    target = serializers.CharField(source='project.target')
    rate = serializers.CharField(source='project.rate')
    reached = serializers.CharField(source='project.reached')
    first_picture = serializers.CharField(
        source='project.projectpics_set.first.picture.url')

    class Meta:
        model = ProjectTags
        fields = ['tag', 'title', 'project', 'category', 'details', 'reached',
                  'rate', 'target', 'start_time', 'end_time', 'first_picture']

# TODO: this should done with category.project_set.all() , it would be faster
# class CategorySerializer(serializers.ModelSerializer):

#     cat_projects = serializers.SerializerMethodField()

#     def get_cat_projects(self, obj):
#         return obj.project_set.first()

#     class Meta:
#         model = Category
#         fields = ['title', 'cat_projects']


class CategorySerializer(serializers.ModelSerializer):
    first_picture = serializers.CharField(
        source='projectpics_set.first.picture.url')

    class Meta:
        model = Project
        fields = ('pk', 'title', 'first_picture')  #
