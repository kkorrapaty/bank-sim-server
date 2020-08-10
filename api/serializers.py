from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.mango import Mango
from .models.user import User
from .models.saving import Saving
from .models.transaction import Transaction

import uuid

class SavingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Saving
    fields = ('id', 'amount', 'owner')

class TransactionSerializer(serializers.ModelSerializer):
  # account = SavingSerializer(read_only=True)
  class Meta:
    model = Transaction
    fields = ('id', 'change_in_amount', 'curr_total', 'account')

class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('name', 'id', 'email', 'password', 'userid')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300, required=True)
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
