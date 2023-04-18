from rest_framework import serializers
from users.models import ClearanceItem, TransactionLog, CustomUser, Office, RegistrarViews, ClearingOffice
from django.utils import timezone
from datetime import datetime
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
# from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer

# class LoginSerializer(RestAuthLoginSerializer):
#     username = None

class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def get_cleaned_data(self):
        return {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

class CustomLoginSerializer(LoginSerializer):
    username = None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class RegistrarViewsSerialize(serializers.ModelSerializer):
    class Meta:
        model = RegistrarViews
        fields = ['cl_itemid',
                  'office_id',
                  'studid',
                  'studfullname',
                  'collcode',
                  'resolve'
                  ]

class ClearanceItemSerialize(serializers.ModelSerializer):
    class Meta:
        model = ClearanceItem
        fields = '__all__'

    def create(self, validated_data):
        validated_data["office"] = self.context["request"].user.office
        validated_data["recorded_by"] = self.context["request"].user.userid
        validated_data["cl_itemid"] = self.context["request"].user.office.office_id + validated_data.get('sy') + validated_data.get('sem') + '-' + str(self.context["request"].user.office.office_serial)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.resolve = 'True'
        instance.resolve_date = str(datetime.now().strftime('%Y-%m-%d'))
        instance.resolve_by = self.context["request"].user.userid

        TransactionLog.objects.create(cl_itemid=ClearanceItem.objects.get(cl_itemid=instance.cl_itemid),
          trans_desc="Resolve Clearance Item",
          trans_recorded=str(datetime.now().strftime('%Y-%m-%d')))
        instance.save()
        return instance

        # instance.resolve = validated_data.get('True')
        # # instance.resolve_date = timezone.now()
        # instance.resolve_by = validated_data.get(self.context["request"].user.userid, instance.resolve_by)
        # instance.save()
        # return instance
        # #self.context["request"].user.userid 

        # # TransactionLog.objects.create(cl_itemid=ClearanceItem.objects.get(cl_itemid=instance.cl_itemid),
        # #   trans_desc="Resolve Clearance Item",
        # #   trans_recorded=timezone.now())
        # instance.save()
        # return instance
        
class InsertClearanceItemSerialize(serializers.ModelSerializer):
    class Meta:
        model = ClearanceItem
        fields = ['cl_itemid',
                'studid',
                'officeid',
                'sem',
                'sy',
                'remarks',
                'resolution',
                'resolve',
                'recorded_by',
                'record_date'
        ]