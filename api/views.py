from django.shortcuts import render, redirect
from django.views import View
from .forms import SelectAccountForm
from django.contrib import messages
from pay.models import UserAccount, TransactionHistory
from django.utils.decorators import method_decorator
from .models import PrivateToken, SaveData
from pay.views import dry
import requests
from rest_framework.response import Response
from django.conf import settings
from .serializers import PaybuddySerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from pay.views import generate_transaction_id
import json
    


class PaybuddyAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print(f"User: {request.user}")
        serializer = PaybuddySerializer(data=request.data)
        if not serializer.is_valid():
            print("Invalid Serializer:", serializer.errors)
            return Response(
                {'msg': 'Invalid data provided', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            upi_id = serializer.validated_data['upi_id']
            PojectIdentity = serializer.validated_data['PojectIdentity']
            name = serializer.validated_data['name']
            amount = serializer.validated_data['amount']
            IdentityOfUser = serializer.validated_data['IdentityOfUser']
            obj = UserAccount.objects.get(upi_id=upi_id)
            obj1 = PrivateToken.objects.get(token=PojectIdentity)
        except ObjectDoesNotExist as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

        SaveData.objects.create(
            upi_id=upi_id,
            PojectIdentity=PojectIdentity,
            name=name,
            amount=amount,
            IdentityOfUser=IdentityOfUser
        )
        return Response(
            {'msg': 'Open your payment app and confirm payment'},
            status=status.HTTP_200_OK
        )


BASE_URL = "http://127.0.0.1:5555/"
class paymentdone(View):
    def get(self, request):
        obj_data = request.session.get('obj_data', None)
        context = {}
        if obj_data:
            try: 
                obj = SaveData.objects.get(id=obj_data)
                print(obj)
                context = {
                    'name': obj.name,
                    'amount': obj.amount,
                    'upi_id': obj.upi_id,
                }
                return render(request, 'api/paymentdone.html', context)
            except ObjectDoesNotExist:
                return redirect('home')
        else:
            return redirect('home')
    
    def post(self, request):
        password = request.POST.get('password')
        user = request.user
       
        obj_data = request.session.get('obj_data', None)
        try: 
            obj = SaveData.objects.get(id=obj_data)
            context = {
                'name': obj.name,
                'amount': obj.amount,
                'upi_id': obj.upi_id,
            }
        except ObjectDoesNotExist:
            return redirect('home')
        try:
            obj = SaveData.objects.get(id=obj_data)
            print(obj.payment_mode)
            user_account = UserAccount.objects.get(user=user, upi_id=obj.upi_id)
            print(user_account.name)
            if user_account.Password == password and user_account.Amount>=obj.amount:
                projectOwnerIdentity = PrivateToken.objects.get(token=obj.PojectIdentity)
                projectOwnerAccount = projectOwnerIdentity.Linkend_account
                print(projectOwnerAccount.name)
                projectOwnerAccountId = projectOwnerAccount.id
                projectOwnerAccount = UserAccount.objects.get(id=projectOwnerAccountId)
                amount = str(obj.amount)
                data = {
                'PojectIdentity': obj.PojectIdentity,
                'amount': amount,
                'IdentityOfUser': obj.IdentityOfUser,
                }
            
                json_data = json.dumps(data)
            
                token = "34523482d68a10b73c7949c5d724e00d8127c116"
                URL = "http://127.0.0.1:5555/PaymentDone/"

               
                headers = {
                  'Content-Type': 'application/json',
                 'Authorization': f'Token {token}',
                }
            
                r = requests.post(url=URL, headers=headers, data=json_data)
                if r.status_code == 200:
                    print('inside')
                    print(r.status_code)
                    messages.success(request, f"{r.json().get('msg')}")
                    user_account.Amount-=obj.amount
                    projectOwnerAccount.Amount+=obj.amount
                    obj.payment_mode = 'Deactive'
                    print(obj.payment_mode)
                    user_account.save()
                    projectOwnerAccount.save()
                    obj.save()
                    transaction_id = generate_transaction_id()
                    TransactionHistory.objects.create(transaction_id=transaction_id,account=user_account, recipient=obj.name,
                    amount=obj.amount, name=user_account.name, payment_method='account')
                    request.session['amount'] = str(obj.amount) 
                    request.session.pop('obj_data', None)
                    return redirect('TransectionSuccess')
                else:
                    print("error")
                    obj.payment_mode = 'Deactive'
                    request.session.pop('obj_data', None)
                    obj.save()
                    error_msg = r.json().get('msg')
                    print(error_msg)
                    msg = 'error try after some time'
                    messages.error(request, f"Payment failed: {msg}")
                    return  redirect('paymentdone')
            else:
                obj.payment_mode = 'Deactive'
                obj.save()
                request.session.pop(obj_data, None)
                msg = "maybe password is not correct or amount is not enougth"
                messages.error(request, f"Payment failed: {msg}")
                return  render(request, 'api/paymentdone.html', context)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            messages.error(request, "An HTTP error occurred while processing your request.")
        except requests.exceptions.JSONDecodeError:
            print(f"Invalid JSON response: {r.text}")
            messages.error(request, "Received an invalid response from the server.")
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, "An unexpected error occurred.")
        print('out')
        return  render(request, 'api/paymentdone.html',context )

            


def paymentcancel(request):
    user = request.user
    obj_data = request.session.get('obj_data', None)
    try:
       obj = SaveData.objects.get(id=obj_data)
       obj.payment_mode = 'Deactive'
       obj.save()
       request.session.pop(obj_data, None)
       return redirect('home')
    except ObjectDoesNotExist:
            return redirect('home')
