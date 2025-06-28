from django.shortcuts import render, redirect
from django.views import View
from .forms import (registrationFrom , UserAccountFrom, AccountPassForm,
TransectionForm, PaymentForm,TransactionFilterForm, MobileRechargeForm, MobileRecharge2Form)
from django.contrib import messages
import random
from .models import UserAccount, TransactionHistory, MobileRechargeHistory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from api.models import SaveData


class homeView(View):
    def get(self, request): 
      usr = request.user
      if request.user.is_authenticated:
        objs = UserAccount.objects.filter(user=usr)
        obj1s = None
        for obj in objs:
            obj1 =  SaveData.objects.filter(upi_id=obj.upi_id, payment_mode='Active')
            if obj1.exists():
             obj1s= obj1
             break 
        if obj1s:
            request.session['obj_data'] = obj1s[0].id  
            return redirect('paymentdone')
        else:
            pass

      form  = TransectionForm()
      RechargeForm = MobileRechargeForm()
      request.session.pop('number', None)
      request.session.pop('plan', None)
      request.session.pop('method', None)
      request.session.pop('recipient', None)
      request.session.pop('amount', None)
      return render(request, 'pay/home.html', {'form': form, 'RechargeForm': RechargeForm})
    
    def post(self, request):
        usr= request.user
        form  = TransectionForm()
        RechargeForm = MobileRechargeForm()
        obj= UserAccount.objects.filter(user=usr)
        if not obj:
            return render(request, 'pay/home.html',{'form': form, 'RechargeForm': RechargeForm, 'msg': "you didn't add any account"})
        form  = TransectionForm(request.POST)
        if form.is_valid():
         
            request.session['method'] = form.cleaned_data['payment_method']
            request.session['recipient'] = form.cleaned_data['recipient']
            return redirect('NextProcess/')
            
        return render(request, 'pay/home.html', {'form':form, 'RechargeForm': RechargeForm})
            
def generate_transaction_id():
    return ''.join([str(random.randint(1, 9)) for _ in range(20)])

def dry(usr, form):
    obj = UserAccount.objects.filter(user=usr)
    if obj:
        form.fields['account'].choices = [(account.id,f'Account Number: {account.Account_number}') for account in obj]
        return form
    else:return None

@method_decorator(login_required, name='dispatch')
class NextProcess(View):
    def get(self, request):
        usr = request.user
        form =PaymentForm()
        obj = dry(usr, form)
        if obj:
          return render(request, 'pay/Nextprocess.html', {'form' :form})
        else: return render(request, 'pay/Nextprocess.html',{'error': "No accounts found!"})

        
    def post(self, request):
        usr = request.user
        obj = UserAccount.objects.filter(user=usr)
        form = PaymentForm(request.POST)
        if obj:
            form.fields['account'].choices = [(account.id, f'Account Number: {account.Account_number}') for account in obj]

        if form.is_valid():
            account_id = form.cleaned_data['account']
            password = form.cleaned_data['password']
            amount = form.cleaned_data['amount']
            reciever = request.session.get('recipient')
            method = request.session.get('method')
            transaction_id = generate_transaction_id()
            if not reciever or not method:
                return redirect('home')

            try:
                account = UserAccount.objects.filter(id=account_id, Password=password, user=usr).first()
                if not account:
                    raise ValueError("Invalid Account or Password")
                if account.Amount < amount:
                    raise ValueError("Your account doesn't have enough balance")

                account.Amount -= amount
                account.save()
                name = account.name  
                request.session['amount'] = str(amount) 

                recipient_account = None
                if method == 'upi':
                    recipient_account = UserAccount.objects.filter(upi_id=reciever).first()
                elif method == "account":
                    recipient_account = UserAccount.objects.filter(Account_number=reciever).first()
                elif method == "phone":
                    recipient_account = UserAccount.objects.filter(Phone_number=reciever).first()

                if recipient_account:
                    recipient_account.Amount += amount
                    recipient_account.save()

                TransactionHistory.objects.create(transaction_id=transaction_id,account=account,recipient=reciever,
                amount=amount, name=name, payment_method=method)
                request.session.pop('method', None)
                request.session.pop('recipient', None)
                return redirect('TransectionSuccess/')
            except ValueError as e:
                return render(request, 'pay/Nextprocess.html', {'form': form, 'error': str(e)})

        return render(request, 'pay/Nextprocess.html', {'form': form})

@login_required
def TransectionSuccess(request):
    amount = request.session.get('amount')
    if amount:
        return render(request, 'pay/TransectionSuccess.html', {'amount':amount})
    else: return redirect('')


class registration(View):
    def get(self, request):
        form  = registrationFrom()
        return render(request, 'pay/registration.html', {'form':form})
    def post(self, request):
        form  = registrationFrom(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'pay/registration.html', {'form':form})


@method_decorator(login_required, name='dispatch')
class AddAccountView(View):

    def get(self, request):
        request.session.pop('name', None)
        request.session.pop('Account_number', None)
        request.session.pop('Phone_number', None)
        form  = UserAccountFrom()
        return render(request, 'pay/AddAccount.html', {'form': form})
    
    def post(self, request):
        form = UserAccountFrom(request.POST)
        if form.is_valid():
            request.session['name'] = form.cleaned_data['name']
            request.session['Account_number'] = form.cleaned_data['Account_number']
            request.session['Phone_number'] = form.cleaned_data['Phone_number']
            return redirect('/AccountPass')
        else:return render(request, 'pay/AddAccount.html', {'form': form})
    

def rendom_upi_id():
    string = ''
    for i in range(10):
        n = random.randrange(0, 10)
        string+=str(n)
    string+='@ilb'
    return string

@method_decorator(login_required, name='dispatch')
class AccountPassView(View):

    def get(self, request):
        form = AccountPassForm()
        return render(request, 'pay/AccountPassword.html',  {'form': form})
    
    def post(self, request):
        form  = AccountPassForm(request.POST)
        if form.is_valid():
            name =  request.session.get('name')
            account_number = request.session.get('Account_number')
            phone_number = request.session.get('Phone_number')
            if not name or not account_number or not phone_number:
                return redirect('/AddAccount')
            usr = request.user
            password = form.cleaned_data['password1'] 
            amount = 10000.00
            upi_id =  rendom_upi_id()
            UserAccount.objects.create( user=usr, name=name, Account_number=account_number,  Phone_number=phone_number, 
             upi_id=upi_id, Password=password,  Amount=amount,)
            request.session.pop('name', None)
            request.session.pop('Account_number', None)
            request.session.pop('Phone_number', None)
            return redirect('/Success')
        else:
            return render(request, 'pay/AccountPassword.html', {'form': form})
    

@login_required
def Success(request):
    return render(request, 'pay/Success.html')


@method_decorator(login_required, name='dispatch')
class AccountDetail(View):
    def get(self, request):
        request.session.pop('selected_account_id', None)
        usr = request.user
        account = UserAccount.objects.filter(user=usr)
        return render(request, 'pay/AccountDetail.html', {'account':account})
    
    def post(self, request):
        account_id = request.POST.get('account_id')
        account_id_for_TH = request.POST.get('account_id_for_TH')
        if account_id_for_TH:
            request.session['selected_account_id'] = account_id_for_TH
            return redirect('/TransectionHistory')
        if account_id:
            request.session['id'] = account_id
            return redirect('/Balance')
        else:return render(request, 'pay/AccountDetail.html', {'account': UserAccount.objects.filter(user=request.user)})

@method_decorator(login_required, name='dispatch')
class BalanceView(View):
    def get(self, request): 
      usr = request.user
      obj = UserAccount.objects.filter(user=usr)
      if obj:
        return render(request, 'pay/Balance.html')
      else:return redirect('/AddAccount')
    
    def post(self, request):
        password = request.POST.get('password')
        usr = request.user
        account_id = request.session.get('id')
        request.session.pop('id', None)
        if not account_id:
              return render(request, 'pay/Balance.html', {'error': 'No account selected.'})

        try:
            account = UserAccount.objects.get(id=account_id, Password=password, user=usr)
            amount = account.Amount
            return render(request, 'pay/Balance.html', {'amount': amount})
        except UserAccount.DoesNotExist:
            return render(request, 'pay/Balance.html', {'error': 'Invalid Password or account'})

        

@method_decorator(login_required, name='dispatch')
class TransectionHistory(View):
    def get(self, request):
        selected_account_id = request.session.get('selected_account_id')
        if selected_account_id:
           transactions = TransactionHistory.objects.filter(account_id=selected_account_id).order_by('-date')
        else: return redirect('/AccountDetail')

        transaction_type = request.GET.get('transaction_type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        min_amount = request.GET.get('min_amount')
        max_amount = request.GET.get('max_amount')
            
        if transaction_type:

            if transaction_type == 'C':
               account = UserAccount.objects.get(id = selected_account_id) 
               ac = account.Account_number
               ph = account.Phone_number
               upi = account.upi_id
               transactions = TransactionHistory.objects.filter(Q(recipient = ac) | Q(recipient = ph) | Q(recipient = upi))
            elif transaction_type == 'D':
                pass

        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if min_amount:
            transactions = transactions.filter(amount__gte=min_amount)
        if max_amount:
            transactions = transactions.filter(amount__lte=max_amount)

        account = UserAccount.objects.get(id = selected_account_id) 
        ac = account.Account_number
        filter_form = TransactionFilterForm(request.GET or None)
        return render(request, 'pay/TransectionHistory.html', {'filter_form': filter_form,
            'transactions': transactions,'ac':ac })

    def post(self, request): 
        yes = request.POST.get('yes')
        if yes:
            request.session.pop('selected_account_id', None)
            return redirect('AccountDetail')
        return render(request, 'pay/TransectionHistory.html')

@login_required
def MobileRecharge(request):
    if request.method == 'POST':
        usr= request.user
        form  = TransectionForm()
        RechargeForm = MobileRechargeForm()
        obj= UserAccount.objects.filter(user=usr)
        if not obj:
            return render(request, 'pay/home.html',{'form': form, 'RechargeForm': RechargeForm, 'msg': "you didn't add any account"})
        RechargeForm = MobileRechargeForm(request.POST)
        if RechargeForm.is_valid():
            request.session['number'] = RechargeForm.cleaned_data['mobile_number']
            request.session['plan'] = RechargeForm.cleaned_data['plan']
            return redirect('MobileRecharge2')
        else:
            TransectionForm_instance = TransectionForm()
            return render(request, 'pay/home.html', { 'form': TransectionForm_instance,
                'RechargeForm': RechargeForm})
    return redirect('')



@method_decorator(login_required, name='dispatch')
class MobileRecharge2(View):
    def get(self, request):
        usr = request.user
        form = MobileRecharge2Form()
        out = dry(usr, form)
        if out is not None:
             return render(request, 'pay/NextProcess.html', {'form' :form})
        else: return render(request, 'pay/NextProcess.html', {'error' :"No account Found"})

    def post(self, request):
        usr = request.user
        obj = UserAccount.objects.filter(user=usr)
        form = MobileRecharge2Form(request.POST)
        if obj:
            form.fields['account'].choices = [(account.id, f'Account Number: {account.Account_number}') for account in obj]
        if form.is_valid():
            account_id = form.cleaned_data['account']
            password = form.cleaned_data['password']
            num = request.session.get('number')
            plan = request.session.get('plan')
            transaction_id = generate_transaction_id()
            try:
                account = UserAccount.objects.filter(id=account_id, Password=password, user=usr).first()
                if not account:
                    raise ValueError("Invalid Account or Password")  
                if plan == '199':
                    account.Amount -= 199  
                elif plan == '399':
                    account.Amount -= 399
                elif plan == '599':
                    account.Amount -= 599
                account.save()
                request.session['amount']  = str(plan)
                MobileRechargeHistory.objects.create( transaction_id=transaction_id, account=account, mobile_number = num,
                    plan=plan, )
                request.session.pop('number', None)
                request.session.pop('plan', None)
                return redirect('MobileRechargeSuccess')
            except ValueError as e:
                return render(request, 'pay/Nextprocess.html', {'form': form, 'error': str(e)})
        return render(request, 'pay/Nextprocess.html', {'form': form})



@login_required
def MobileRechargeSuccess(request):
    amount = request.session.get('amount')
    if amount:
      return render(request, 'pay/MobileRechargeSuccess.html', {'amount':amount})
    else: return redirect('')





