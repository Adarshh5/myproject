from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
#from django.contrib.auth import password_validation
from .models import UserAccount, TransactionHistory , MobileRechargeHistory



class registrationFrom(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
       
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class' :'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


def Account_number(value):
    if not value.isdecimal() or len(value) != 12:
        raise forms.ValidationError("Account Number must be exactly 12 digits long and contain only numbers.")

def Phone_number(value):
    if not value.isdecimal() or len(value) != 10:
        raise forms.ValidationError("Phone Number must be exactly 10 digits long and contain only numbers.")

def password(value):
    if not value.isdecimal() or len(value) != 6:
        raise forms.ValidationError("Password must be exactly 6 digits long and contain only numbers.")


class UserAccountFrom(forms.ModelForm):
    Account_number = forms.CharField(required=True,validators=[Account_number], widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone_number = forms.CharField(required=True, validators=[Phone_number], widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:

        model  = UserAccount
        fields = ['name', 'Account_number', 'Phone_number']
        labels = {'name': 'Name', 'Account_number': 'Account Number', 'Phone_number': 'Phone Number'}
        widgets = {'name': forms.TextInput(attrs=  {'class': 'form-control'}) }


class AccountPassForm(forms.Form):
    password1 = forms.CharField(validators=[password],label="Password1", required=True, widget=forms.PasswordInput(attrs={'class': "form-control"}) )
    password2 = forms.CharField(validators=[password],label="Passwrd again",required=True, widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



class TransectionForm(forms.ModelForm):
    class Meta:
        model =  TransactionHistory
        fields = ['payment_method', 'recipient']
        labels = {'recipient': 'Recipient',  'payment_method': 'Payment Method'}
        widgets = {'recipient': forms.TextInput(attrs=  {'class': 'form-control'}),
                    'payment_method': forms.Select(attrs=  {'class': 'form-control'})  }
        
    def clean(self):
        cleaned_data = super().clean()
        recipient = cleaned_data.get("recipient")
        method = cleaned_data.get('payment_method')

        if method  == "upi":
           if not recipient.endswith('@ilb'):
              raise forms.ValidationError("please enter correct UPi Id")
           if not UserAccount.objects.filter(upi_id=recipient).exists():
              raise forms.ValidationError('This is not a valid Upi_id')
        if method == 'account':

           if not recipient.isdecimal() or len(recipient) !=  12 :
                raise forms.ValidationError("please enter correct 12 digit account number ")
   
        if  method  == "phone":
           if not recipient.isdecimal() or len(recipient) != 10 :
               raise forms.ValidationError("please enter correct 10 digit Phone number ")
        
        return cleaned_data


class PaymentForm(forms.Form):
    account = forms.ChoiceField(widget=forms.RadioSelect, choices=[], label='Select Account')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': "Enter Amount", "class": "form-control my-3"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class':'form-control my-2'}))


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and (amount > 10000.00 or amount <= 0):
            raise forms.ValidationError("Minimum transaction limit is 1 and maximum is 10,000.00!")
        return amount
    
    

class TransactionFilterForm(forms.Form):
    transaction_type = forms.ChoiceField(choices=[('D', 'Debit'), ('C', 'Credit')],required=False,label="Transaction Type",
    widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField( required=False,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    label="Start Date")
    end_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),label="End Date")
    min_amount = forms.DecimalField(required=False,max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={'class': 'form-control'}),
    label="Minimum Amount")
    max_amount = forms.DecimalField(required=False,max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={'class': 'form-control'}),
    label="Maximum Amount")


class MobileRechargeForm(forms.ModelForm):
    mobile_number = forms.CharField(required=True, validators=[Phone_number], widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model =  MobileRechargeHistory
        fields = ['plan']
        labels = {'mobile_number': 'Mobile Number',  'plan': 'Plan'}
        widgets = {'plan': forms.Select(attrs={'class': 'form-control'})}
        


class MobileRecharge2Form(forms.Form):
    account = forms.ChoiceField(widget=forms.RadioSelect, choices=[], label='Select Account')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class':'form-control my-2'}))