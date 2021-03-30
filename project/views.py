from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from .models import (Project, ProjectPics, ProjectTags, Donation, UserDonationProject, Rate, Category,
                     UserRateProject, Comment, UserCommentProject, ReportedComments, ReportedProjects, FeaturedProjects)
from .forms import ProjectCreateForm
import accounts.models as acc_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models.aggregates import Sum
from django.contrib.auth.mixins import UserPassesTestMixin
import os
from django.contrib import messages


def home(request):
    latest_projects = Project.objects.all().order_by('-start_time')[:5]
    featured_projects = FeaturedProjects.objects.all()[:5]
    highest_projects = Project.objects.all().order_by('-rate')[:5]
    return render(request, 'project/base.html', {'latest_projects': latest_projects,
                                                 'featured_projects': featured_projects,
                                                 'highest_projects': highest_projects})


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


class ProjectDetailView(DetailView):
    template_name = 'project/project_details.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = (super().get_context_data)(**kwargs)
        context['project_owner'] = acc_models.UserProject.objects.get(
            project=(self.object)).user
        context['project_comments'] = self.object.usercommentproject_set.all()
        context['rate'] = self.object.rate
        context['target'] = self.object.target
        context['reached'] = self.object.reached
        context['similar_projects'] = self.object.category.project_set.all().order_by('?')[
            :4]
        return context


@login_required
def my_projects(request):
    efc_user = acc_models.ECFUser.objects.get(user=request.user)
    projs = efc_user.userproject_set.all()

    return render(request, 'project/my_projects.html', {'projs': projs})


@login_required
def donate(request, project):
    proj = Project.objects.get(pk=project)
    project_target = proj.target
    project_reached = proj.reached
    amount = request.POST['amount']
    proj_pk = int(project)

    if int(amount) + int(project_reached) <= int(project_target):
        proj.reached += int(amount)
        proj.save()
        donation = Donation.objects.create(amount=amount)
        ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
        UserDonationProject.objects.create(
            donation=donation, user=ecf_user, project=proj)
        messages.add_message(request, messages.SUCCESS,
                             'Thank you for donation ♥', extra_tags='alert alert-success')
    else:
        messages.add_message(request, messages.ERROR, 'You can donate only up to target!',
                             extra_tags='alert alert-danger donate-err')

    return redirect(reverse('project:project_details', args=(proj_pk,)))


@login_required
def my_donations(request):
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    user_donations = ecf_user.userdonationproject_set.all()

    return render(request, 'project/donations.html', {'dons': user_donations})


@login_required
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
    proj_pk = int(project)

    proj.save()
    messages.add_message(request, messages.SUCCESS,
                         'Thanks for rating', extra_tags='alert alert-info')

    return redirect(reverse('project:project_details', args=(proj_pk,)))


@login_required
def comment(request, project):
    comment_content = request.POST['comment']
    comnt = Comment.objects.create(content=comment_content)
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    proj = Project.objects.get(pk=project)
    UserCommentProject.objects.create(
        user=ecf_user, comment=comnt, project=proj)

    return redirect(reverse('project:project_details', args=(project,)))


@login_required
def report_comment(request, c_pk, project):
    comment = Comment.objects.get(pk=c_pk)
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    ReportedComments.objects.create(comment=comment, reporter=ecf_user)
    messages.add_message(request, messages.SUCCESS,
                         'Thanks for report, we will review this comment', extra_tags='alert alert-warning')

    return redirect(reverse('project:project_details', args=(project,)))


@login_required
def report_project(request, project):
    ecf_user = acc_models.ECFUser.objects.get(user=(request.user))
    proj = Project.objects.get(pk=project)
    ReportedProjects.objects.create(reporter=ecf_user, project=proj)
    messages.add_message(request, messages.SUCCESS,
                         'Thanks for report, we will review this project', extra_tags='alert alert-warning')

    return redirect(reverse('project:project_details', args=project))


class DeleteProjectView(UserPassesTestMixin, DeleteView):
    model = Project

    def target_quart(self):
        reached = self.get_object().reached
        target = self.get_object().target
        return (reached/target)*100 < 25

    def test_func(self):
        user_project = acc_models.UserProject.objects.get(
            project=self.get_object())
        ecf_user = acc_models.ECFUser.objects.get(user=(self.request.user))
        return user_project.user == ecf_user and self.target_quart()

    def get_success_url(self):
        return reverse_lazy('project:my_projects')


class AllProjects(ListView):
    model = Project
    template_name = 'project/projects_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = (super().get_context_data)(**kwargs)
        context['cats'] = Category.objects.all()
        return context
