from rest_framework import serializers
from .models import *

class React(serializier.ModelSerializer):
    class Meta:
        model = React
        fields = ['','']