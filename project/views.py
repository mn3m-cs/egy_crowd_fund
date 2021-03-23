from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DetailView
from .models import (Project, ProjectPics, ProjectTags, Donation, UserDonationProject, Rate,
                     UserRateProject, Comment, UserCommentProject, ReportedComments, ReportedProjects)
from .forms import ProjectCreateForm
import accounts.models as acc_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.aggregates import Sum


def home(request):
    return render(request, 'project/base.html')


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'project/project_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        proj = self.object
        if form.is_valid():
            form.save(commit=True)
            ecf_user = acc_models.ECFUser.objects.get(user=(self.request.user))
            acc_models.UserProject.objects.create(user=ecf_user, project=proj)

        tags = self.request.POST['tags']
        tags_list = tags.split('#')
        for tag in tags_list:
            if tags_list.index(tag) != 0:
                ProjectTags.objects.create(project=proj, tag=tag)

        for pic in self.request.FILES.getlist('pictures'):
            ProjectPics.objects.create(project=proj, picture=pic)
        else:
            return super().form_valid(form)

# TODO: add testmixin


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'project/project_details.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = (super().get_context_data)(**kwargs)
        context['project_owner'] = acc_models.UserProject.objects.get(
            project=(self.object)).user
        context['project_comments'] = self.object.usercommentproject_set.all()
        context['rate'] = self.object.rate
        return context


@login_required
def my_projects(request):
    efc_user = acc_models.ECFUser.objects.get(user=request.user)
    projs = efc_user.userproject_set.all()

    return render(request, 'project/my_projects.html', {'projs': projs})


@login_required  # TODO: add test
def donate(request, project):
    # TODO: return message
    proj = Project.objects.get(pk=project)
    project_target = proj.target
    project_reached = proj.reached
    amount = request.POST['amount']

    if int(amount) + int(project_reached) <= int(project_target):

        donation = Donation.objects.create(amount=amount)
        ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
        UserDonationProject.objects.create(
            donation=donation, user=ecf_user, project=proj)
    else:
        print('over')  # TODO: return message
    return redirect(reverse('project:project_details', args=project))


def my_donations(request):
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    user_donations = ecf_user.userdonationproject_set.all()

    return render(request, 'project/donations.html', {'dons': user_donations})

# TODO: add tests to all views


def rate(request, project):
    rate_val = request.POST['rate']
    rate = Rate.objects.create(rate=rate_val)
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    proj = Project.objects.get(pk=project)
    UserRateProject.objects.create(rate=rate, project=proj, user=ecf_user)
    proj.rates_number += 1
    rates = [r.rate.rate for r in proj.userrateproject_set.all()]
    rates_sum = sum(rates)
    proj.rate = rates_sum / proj.rates_number

    proj.save()

    return redirect(reverse('project:project_details', args=project))


def comment(request, project):
    comment_content = request.POST['comment']
    comnt = Comment.objects.create(content=comment_content)
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    proj = Project.objects.get(pk=project)
    UserCommentProject.objects.create(
        user=ecf_user, comment=comnt, project=proj)

    return redirect(reverse('project:project_details', args=project))


def report_comment(request,c_pk,project):
    comment = Comment.objects.get(pk=c_pk)
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    ReportedComments.objects.create(comment=comment,reporter=ecf_user)
    
    return redirect(reverse('project:project_details', args=project))




def report_project(request, project):
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    proj = Project.objects.get(pk=project)
    ReportedProjects.objects.create(reporter=ecf_user, project=proj)

    return redirect(reverse('project:project_details', args=project))
