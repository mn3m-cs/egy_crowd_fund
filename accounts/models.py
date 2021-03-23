from django.db import models
from django.contrib.auth.models import User


class ECFUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pics', verbose_name='Profile Picture', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=20)  # TODO: make list
    city = models.CharField(max_length=50)  # TODO:
    fb_profile = models.URLField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name


class UserPhone(models.Model):
    user = models.ForeignKey(ECFUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.phone


class UserProject(models.Model):
    user = models.ForeignKey(ECFUser, on_delete=models.CASCADE)
    # user lazy_related_operation to avoid circular import
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '_' + str(self.project)
