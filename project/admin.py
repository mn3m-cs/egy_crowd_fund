from django.contrib import admin

from .models import Category,Project,ProjectPics,ProjectTags,Comment,UserCommentProject

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(ProjectPics)
admin.site.register(ProjectTags)
admin.site.register(Comment)
admin.site.register(UserCommentProject)
