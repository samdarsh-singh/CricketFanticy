from email.policy import default
from rest_framework import serializers
from .models import User,Wallet,Transaction,Wheel
import pyotp
import random
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile', 'name', 'username','profile_id','profile','referral']
        read_only_fields = ['id','name', 'username', 'profile_id','profile','referral']

    def create(self, validated_data,**extra_fields):
        instance = self.Meta.model(**validated_data)
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords, k=6)))
        mywordss = "123456789abcdefghijklmnopqrstABCDEFGHIJKLMNOPQRSTUVWXYZ"
        referral = "" + str(''.join(random.choices(mywordss, k=8)))
        # path = os.path.join(BASE_DIR, 'static/images')
        # dir_list = os.listdir(path)
        # random_logo = random.choice(dir_list)


        if self.Meta.model.objects.filter(**validated_data).exists():
            instance = self.Meta.model.objects.filter(**validated_data).last()
            instance.otp = str(random.randint(1000, 9999))
            instance.save()
        else:
            instance = self.Meta.model(**validated_data)
            instance.otp = str(random.randint(1000, 9999))
            instance.username = res
            instance.name = str(f"{instance.mobile[0:2]}****{instance.mobile[7:10]}")
            # instance.name = instance.mobile
            instance.profile_id = instance.profile_id
            instance.profile = instance.profile
            instance.id = instance.id
            instance.referral = referral
            instance.save()
        return instance


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp','referral']
        read_only_fields = ['otp','referral']


class UserGetProfileChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'username', 'profile', 'profile_id']


class UserProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username', 'profile', 'profile_id']


class GetTotalwalletserializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','total_amount','deposit_cash','winning_cash','withdraw_amount','Bonus']


class walletserializer_add(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','deposit_cash','winning_cash']


class walletserializer_deduct(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','total_amount','deposit_cash','winning_cash','withdraw_amount']


class GetResponceSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_status(self, obj):
        return True

    def get_message(self, obj):
        return "success"


class GetResponceRedeemSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_status(self, obj):
        return True

    def get_message(self, obj):
        return "User can Redeem Someone's Referral code"


class Transactionserializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['total_amount', 'deposit_cash', 'winning_cash','withdraw_amount','Bonus']
        # read_only_fields = ('winning_cash',)


class TransactionHistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'description','transaction_method', 'date', 'time']
        # read_only_fields = ('wallet',)


class Getreferralserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['referral']


class RedeemReferralcodeserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['referral']


class Bonusserializer(serializers.ModelSerializer):
    class Meta:
        model = Wheel
        fields = ['wheels_index']


class Bonusserializer12(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['total_amount', 'deposit_cash', 'winning_cash','withdraw_amount']


