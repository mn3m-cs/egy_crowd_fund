from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from .models import Project, ProjectPics, ProjectTags
from .forms import ProjectCreateForm
import accounts.models as acc_models
from django.contrib.auth.mixins import LoginRequiredMixin

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


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/project_details.html'

    def get_context_data(self, **kwargs):
        context = (super().get_context_data)(**kwargs)
        context['project_owner'] = acc_models.UserProject.objects.get(project=(self.object)).user
        return context