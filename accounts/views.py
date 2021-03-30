from django.shortcuts import redirect, render
from django.views.generic import FormView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import six
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.forms.models import model_to_dict
# from django.core.files.storage import FileSystemStorage
import datetime

from .models import ECFUser, UserPhone
from .forms import ECFUserForm, UpdateProfile
from .tokens import account_activation_token
import time


class RegisterView(FormView):
    form_class = ECFUserForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        usrname_form = self.request.POST['username']
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activate your ECF account.'

        self.request.session['token_creation_time'] = time.time()

        message = render_to_string('accounts/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        # return HttpResponse('Please confirm your email address to complete the registration')

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
        for phone in phones:
            phone = self.request.POST.get(phone)
            UserPhone.objects.create(user=ecf_user, phone=phone)
        messages.add_message(self.request, messages.INFO,
                             'Thank you for registeration, please check your email for activation link.', extra_tags='alert alert-warning')

        return redirect(reverse('project:home'))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        token_creation_time = request.session.get('token_creation_time')
        time_now = time.time()
        diff = time_now - token_creation_time

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token)  and diff <= 86400:
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(
            request, messages.INFO, 'Thank you for your email confirmation', extra_tags='alert alert-success')
        return redirect('project:home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
            # TODO: delete old image
            # TODO: edit picture filed to be like fb change
            additional_info = request.POST['additional_info']
            ECFUser.objects.update(birth_date=birth_date, country=country,
                                   additional_info=additional_info,
                                   city=city, fb_profile=fb_profile)
            if 'profile_pic' in request.FILES.keys():
                profile_pic = request.FILES['profile_pic']
                ecf_user = ECFUser.objects.get(user=request.user)
                ecf_user.profile_pic = profile_pic
                ecf_user.save()

            return redirect(reverse('project:home'))
    else:
        u = ECFUser.objects.get(user=request.user)

        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        # form = UpdateProfile(data)
        ecf_dict = model_to_dict(u)
        ecf_dict['first_name'] = request.user.first_name
        ecf_dict['last_name'] = request.user.last_name

        form = UpdateProfile(initial=ecf_dict)
    return render(request, 'accounts/edit_profile.html', {'form': form, })


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('project:home')
    template_name = 'accounts/user_confirm_delete.html'
