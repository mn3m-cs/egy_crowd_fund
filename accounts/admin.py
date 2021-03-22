from django.contrib import admin
from .models import ECFUser,UserPhone,UserProject
# Register your models here.
admin.site.register(ECFUser)
admin.site.register(UserPhone)
admin.site.register(UserProject)
