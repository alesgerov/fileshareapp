from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import File
from django.forms import ModelForm
#from .models import RequestPull

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class UploadFileForm(ModelForm):
    
    # title = forms.CharField(max_length=200)
    # content=forms.CharField(max_length=20000)
    # file = forms.FileField() 
    class Meta:
        model=File
        fields=['title','content','file']

    # showPermit=forms.MultipleChoiceField(choices=[User], required=False)
    # commentPermit=forms.MultipleChoiceField(choices=[User], required=False)
    

    





# class GetReq(forms.ModelForm):
#     class Meta:
#         model = RequestPull
#         fields = ['clientname','ip_address']