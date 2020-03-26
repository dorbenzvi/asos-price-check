from django import forms
from pricecheck.models import Users,Alert
from django.contrib.auth.models import  User



class createAlert(forms.Form):
    product_name = forms.CharField(required=True, max_length=100)
    product_url = forms.URLField(required=True)


class registerForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'


class deleteAlert(forms.ModelForm):
    class Meta:
        model = Alert
        fields ='__all__'

class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(),min_length=7)


    class Meta():
        model = User
        fields = ('username','email','password')


