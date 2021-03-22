from django import forms
from .models import Category,Project,ProjectPics,ProjectTags,Comment,UserCommentProject

class ProjectCreateForm(forms.ModelForm):
    pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Must be separated by #'}))

    class Meta:
        model = Project
        fields = ('category','title','details','start_time','end_time','target')
