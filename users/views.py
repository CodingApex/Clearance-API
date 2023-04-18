from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from users.models import ClearanceItem, RegistrarViews, Office, CustomUser, TransactionLog
from users.serializer import ClearanceItemSerialize, RegistrarViewsSerialize, InsertClearanceItemSerialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Create your views here.

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
    client_class = OAuth2Client

@api_view(['GET'])
def api_root(request):
    return Response({
        'ClearanceItem': reverse('clerk', request=request),
        'RegistrarView': reverse('registrar', request=request)
    })

# /Registrar/
class APIRegistrarViews(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RegistrarViews.objects.raw('select * from curriculum.registrar_view()')
    serializer_class = RegistrarViewsSerialize

# /Clerk/
class APIClerkView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClearanceItemSerialize

    def get_queryset(self):
        office_id = self.request.user.office
        return ClearanceItem.objects.filter(office=office_id)

# /Clerk/<str:pk>/
class APIClerkUpdate(generics.RetrieveUpdateAPIView):
    queryset = ClearanceItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClearanceItemSerialize

# class APIClerkViewDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ClearanceItem.objects.all()
#     serializer_class = ClearanceItemSerialize

    # def perform_create(self, serializer):
    #     serializer.save(office=Office.objects.get(officeid=self.request.user.officeid),
    #     recorded_by=self.request.user.userid)