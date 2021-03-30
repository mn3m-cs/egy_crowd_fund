from django import forms
from .models import ECFUser, UserPhone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.utils.functional

class ECFUserForm(UserCreationForm):
    profile_pic = forms.ImageField()
    birth_date = forms.DateField()
    country = forms.CharField(max_length=20)
    city = forms.CharField(max_length=50)
    fb_profile = forms.URLField()
    phone1 = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UpdateProfile(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(UpdateProfile, self).__init__()
        # args[0] is the use in get method
        # args[0] is querydict in POST method

        # if isinstance(args[0],django.utils.functional.SimpleLazyObject):
        #     self.fields['first_name'].initial = args[0].first_name
        #     self.fields['last_name'].initial = args[0].last_name
        #     ecf_user = ECFUser.objects.get(user=args[0])
        #     self.fields['birth_date'].initial = ecf_user.birth_date
        #     self.fields['country'].initial = ecf_user.country
        #     self.fields['city'].initial = ecf_user.city
        #     self.fields['fb_profile'].initial = ecf_user.fb_profile
        #     self.fields['additional_info'].initial = ecf_user.additional_info


    first_name = forms.CharField(required=False)
    last_name = forms.CharField()
    profile_pic = forms.ImageField(required=False)
    birth_date = forms.DateField()
    country = forms.CharField(max_length=20)
    city = forms.CharField(max_length=50)
    fb_profile = forms.URLField()
    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    # phone1 = forms.CharField(max_length=15)
