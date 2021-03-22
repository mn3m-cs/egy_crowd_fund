from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

import accounts.models as acc_models


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    details = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    target = models.PositiveSmallIntegerField()
    reached = models.PositiveSmallIntegerField(default=0)
    rate = models.SmallIntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ],
        null=True)
    rates_number = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project:home') #TODO:


class ProjectPics(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    picture = models.ImageField()

    def __str__(self):
        return str((self.picture))


class ProjectTags(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)

    def __str__(self):
        return str(self.project) + ' ' + str(self.tag)


class Comment(models.Model):
    content = models.TextField()
    
    def __str__(self):
        return self.content


class UserCommentProject(models.Model):
    user = models.ForeignKey(acc_models.ECFUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' SAY ' + str(self.comment) + ' ON ' + str(self.project)

class Donation(models.Model):
    amount = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.amount)

class UserDonationProject(models.Model):
    donation = models.ForeignKey(Donation,on_delete=models.CASCADE)
    user = models.ForeignKey(acc_models.ECFUser,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.donation)

class Rate(models.Model):
    rate = models.SmallIntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rate)

class UserRateProject(models.Model):
    rate = models.ForeignKey(Rate,on_delete=models.CASCADE)
    user = models.ForeignKey(acc_models.ECFUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rate)


class ReportedProjects(models.Model):
    reporter = models.ForeignKey(acc_models.ECFUser,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reporter) + ' REPORTED '+ str(self.project)

class ReportedComments(models.Model):
    reporter = models.ForeignKey(acc_models.ECFUser,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reporter) + ' REPORTED '+ str(self.comment)
