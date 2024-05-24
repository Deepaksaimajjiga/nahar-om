import random, requests

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

# jwt token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import strip_tags

# Imports from custom_admin
from .models import *
from django.core.mail import EmailMessage

from django.utils.crypto import get_random_string
from .models import *



def SendEmail(link, purpose, email, attachment_path=None):
    """
    Send an email with a given referral link and purpose.

    Parameters:
    - link (str): The referral link to be included in the email.
    - purpose (str): The purpose of the email, used to select the template. 
    - email (str): The recipient's email address.
    - attachment_path (str, optional): The file path of the attachment if any.
    """
    try:
        template = EmailTemplate.objects.filter(purpose=purpose).first()

        subject = template.subject
        message = template.body.replace("{{referal_link}}", link)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        email_message = EmailMessage(
            subject,
            strip_tags(message),
            from_email,
            recipient_list,
        )

        # Attach the document if attachment_path is provided
        if attachment_path:
            email_message.attach_file(attachment_path)

        email_message.send(fail_silently=False)

        return "Sent"
    except Exception as e:
        print(f"Email not sent {e}")
        return "Not Sent"
    
def generate_voucher():
    # Generates a unique voucher code
    return Voucher.objects.create(
        code=get_random_string(8),
        discount_amount=10.00,
    )

def handle_referral(referred_user, referred_by):
    # Create referral relationship
    ReferalInfo.objects.create(uid=referred_user, refered_by=referred_by)

    # Generate vouchers for both users
    referred_user_voucher = generate_voucher()
    referred_by_voucher = generate_voucher()

    # Add vouchers to their wallets
    referred_user.referral_wallet.vouchers.add(referred_user_voucher)
    referred_by.referral_wallet.vouchers.add(referred_by_voucher)