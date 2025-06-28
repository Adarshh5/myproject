
from django import forms
from django.contrib.auth.models import User 
from django.utils.translation import gettext, gettext_lazy as _

class SelectAccountForm(forms.Form):
    account = forms.ChoiceField(widget=forms.RadioSelect, choices=[], label='Select Account')