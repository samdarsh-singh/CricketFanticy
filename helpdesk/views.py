from django.shortcuts import render
from rest_framework.decorators import APIView
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from cart.models import User
from django.core.mail import send_mail
#from rest_framework import viewsets
from django.conf import settings
from rest_framework.permissions import AllowAny

class TicketAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TicketSerializer
    def post(self, request,pk):
        content = request.data['content']
        qp = User.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            x = {'token': instance.token,'content': instance.content}
            instance.user = qp
            instance.token = instance.token
            instance.content = instance.content
            instance.email = instance.email
            instance.save()
            subject = instance.content
            email_from = settings.EMAIL_HOST_USER
            message = "Token : "+str(instance.token)+"\nQuery : "+str(instance.content)
            recipient_list = ['support@heavenofgamers.com']
            send_mail(subject,message, email_from, recipient_list)
            return JsonResponse({"status":True,"message": "success", 'token': instance.token,'content': instance.content}, safe =False)
        else:
            return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)