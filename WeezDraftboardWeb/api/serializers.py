from rest_framework import serializers
from .models import *
"""
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
"""
class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adp
        fields = '__all__'