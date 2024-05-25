from django.shortcuts import render
from .models import *
from .template import *
from .utility import SendEmail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

# Create your views here.

def register(request, referral_code):
    referral = get_object_or_404(ReferalInfo, referral_code=referral_code)
    if request.method == 'POST':
        # Assumed form validation and user creation logic here
        uid = request.POST.get('user_ID')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        entity_type = request.POST.get('entity_type')
        user = CustomUser.objects.create_user(uid,phone_number,password,company_name,entity_type) # Create user logic
        user.save()
        
        referral.referrer = CustomUser.objects.get(uid=referral_code)
        referral.referred_user = user
        referral.save()

        # Create referral vouchers
        Voucher.objects.create(user=referral.referrer, code=get_random_string(8), discount_amount=50.00)
        Voucher.objects.create(user=user, code=get_random_string(8), discount_amount=50.00)

        # Create or update referral wallets
        ReferralWallet.objects.get_or_create(user=referral.referrer)
        ReferralWallet.objects.get_or_create(user=user)
        
        # Redirect to some success page
        return HttpResponse("REFERRAL VOUCHER & REFERRAL WALLET SUCCESSFUL!")
    return HttpResponse("HELLO WORLD!")

@login_required
def referral_wallet(request):
    wallet = get_object_or_404(ReferralWallet, user=request.user)
    return render(request, 'referrals/wallet.html', {'wallet': wallet})



class SampleView(APIView):
    def get(self,request):
        try:
            link = "http://127.0.0.1:8000/api/register?referralcode=" + request.user.uid
            email = "naturalstarnani654@gmail.com"
            purpose = "Referral link"
            SendEmail(
                link=link,
                email=email,
                purpose=purpose,
            #     attachment_path=model_instance.file.path,
            )
            return Response("1234")
        except Exception as e:
            print(f"Error Sending to buyer {e}")
            return Response("1234")