from django.shortcuts import render
from .models import *
from .utility import SendEmail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
class SampleView(APIView):
    def get(self,request):
        try:
            link = ""
            email = "vickytilotia12344@gmail.com"
            purpose = "Refferal"
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