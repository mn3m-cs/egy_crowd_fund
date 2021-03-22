from django.contrib import admin

from .models import (Category,Project,ProjectPics,ProjectTags,Comment,UserCommentProject,
Donation,UserDonationProject,ReportedProjects,ReportedComments,Rate,UserRateProject)

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(ProjectPics)
admin.site.register(ProjectTags)
admin.site.register(Comment)
admin.site.register(UserCommentProject)
admin.site.register(UserDonationProject)
admin.site.register(UserRateProject)
admin.site.register(Rate)
admin.site.register(ReportedComments)
admin.site.register(ReportedProjects)


class DonationAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Donation,DonationAdmin)