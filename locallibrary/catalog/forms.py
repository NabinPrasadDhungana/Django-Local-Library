import datetime

from django import forms
from django.forms.widgets import DateInput

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm
from .models import *
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.views import LoginView


# class CustomLoginView(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'registration/login.html'

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
        widgets = {
            'due_back': DateInput(attrs={'type': 'date'}),
        }
