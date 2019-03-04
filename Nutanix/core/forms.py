from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from link_it.models import Affiliates,Bitlinks,Affiliates_login

class DetailsForm(forms.ModelForm):

    class Meta:
        fields = ('n', 'p')


# class BitlinkForm(forms.ModelForm):
#
#     class Meta:
#         model = Bitlinks
#         fields = {'long_link'}
#
# class AffiliateLoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = Affiliates_login
#         fields = ('username','password')