from django import forms
from .models import *


class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Имя', required=False,
                           widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label='Фамилия', required=False,
                                widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.CharField(label='email', required=False, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    # region = forms.CharField(label='Область', required=False,
    # widget=forms.SelectMultiple(attrs={"class": 'form-control'}))
    
    class Meta(object):
        model = Person
        fields = ('name', 'last_name', 'email', 'region', 'phones')

        
class NewPhoneForm(forms.ModelForm):
    number = forms.CharField(label='Номер', required=True, widget=forms.TextInput(attrs={"class": 'form-control'}))
    
    class Meta(object):
        model = Phone
        fields = ('number',)

class PersonForm1(forms.Form):
    name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.CharField(label='Email', required=False, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    region = forms.ModelChoiceField(label='Область',queryset=Region.objects.all(),
                        empty_label=None, widget=forms.RadioSelect(attrs={"class": 'form-control'}))
                        
    phones = forms.ModelMultipleChoiceField(label='Дополнительные телефоны', required=False,  queryset=Phone.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class": 'form-control'}))
    
    phone = forms.CharField(label='Телефон', required=False,
                           widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Номер телефона должен начинаться с 0 и иметь десять цифр, например 0123456789'}))
                           
    
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Person.objects.filter(email=email).count()
        if qs>0:
            msg = "Этот email уже используется!"
            raise forms.ValidationError(msg)
        return email
    
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone[0] !='0':
            msg = "Номер должен начинаться с 0!"
            raise forms.ValidationError(msg)
        if len(phone) <10:
            msg = "Номер должен быть длинной в 10 цифр!"
            raise forms.ValidationError(msg)
        phone = phone[:10]
        try:
            _ = int(phone)
                
        except ValueError:
            msg = "Телефон должен содержать только цифры!"
            raise forms.ValidationError(msg)
        
        return phone
