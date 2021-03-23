from django.shortcuts import redirect, render
from django.views.generic import FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ECFUser, UserPhone
from .forms import ECFUserForm, UpdateProfile
from django.urls import reverse, reverse_lazy


class RegisterView(FormView):
    form_class = ECFUserForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        print('valid')
        usrname_form = self.request.POST['username']
        form.save(commit=True)
        user = User.objects.get(username=usrname_form)

        birth_date = self.request.POST['birth_date']
        country = self.request.POST['country']
        city = self.request.POST['city']
        ecf_user = ECFUser.objects.create(user=user,
                                          birth_date=birth_date,
                                          country=country,
                                          city=city,
                                          )

        if 'profile_pic' in self.request.FILES.keys():
            ecf_user.profile_pic = self.request.FILES['profile_pic']

        if 'fb_profile' in self.request.POST.keys():
            ecf_user.fb_profile = self.request.POST['fb_profile']

        ecf_user.save()

        phones = [
            name for name in self.request.POST if name.startswith("phone")]
        print(phones)
        print('here')
        for phone in phones:
            phone = self.request.POST.get(phone)
            UserPhone.objects.create(user=ecf_user, phone=phone)

        return redirect(reverse('accounts:register'))


# class EditProfile(LoginRequiredMixin, UpdateView):
#     model = ECFUser
#     fields = ('country', 'city', 'profile_pic', 'fb_profile')
#     template_name = 'accounts/edit_profile.html'
#     success_url = reverse_lazy('project:home')


def edit_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            p = User.objects.update(first_name=first_name, last_name=last_name)

            birth_date = request.POST['birth_date']
            country = request.POST['country']
            city = request.POST['city']
            fb_profile = request.POST['fb_profile']
            profile_pic = request.FILES['profile_pic']
            # TODO: delete old image
            # TODO: edit picture filed to be like fb
            additional_info = request.POST['additional_info']
            ECFUser.objects.update(birth_date=birth_date, country=country,
                                   additional_info=additional_info,
                                   profile_pic=profile_pic, city=city, fb_profile=fb_profile)
    else:
        form = UpdateProfile(request.user)
        # user = ECFUser.objects.get(user=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form,
                                                          })
