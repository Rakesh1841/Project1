from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = [ 'title', 'discription' ]    


class DateInput(forms.DateInput):
    input_type = 'date' 

class Homework_Form(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description', 'due','is_finished'] 

class DashboardForms(forms.Form):
    text =  forms.CharField(max_length=200, label= "Search")

class Todo_Form(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class ConversionForm(forms.Form):
    CHOICES =[('length','length'),('mass','mass')]
    measurement = forms.ChoiceField(choices= CHOICES,widget=forms.RadioSelect)


class conversionLengthForm(forms.Form):
    CHOICES = [('Yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(attrs={'type':'number','placeholder':'enter the number'}))
    measure1 = forms.CharField (label='',widget=forms.Select (choices= CHOICES))
    measure1 = forms.CharField (label='',widget=forms.Select (choices= CHOICES))

class conversionMassForm(forms.Form):
    CHOICES = [('pound','pound'),('kilogram','kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(attrs={'type':'number','placeholder':'enter the number'}))
    measure1 = forms.CharField (label='',widget=forms.Select (choices= CHOICES))
    measure1 = forms.CharField (label='',widget=forms.Select (choices= CHOICES))


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
