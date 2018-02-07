
from django import forms
from .models import *

class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.CharField(label='email', required=False, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    #region = forms.CharField(label='Область', required=False, widget=forms.SelectMultiple(attrs={"class": 'form-control'}))
    
    
    
    class Meta(object):
        model = Person
        fields = ('name','last_name','email', 'region', 'phones')