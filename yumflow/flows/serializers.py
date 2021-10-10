from django.db import models
from django.db.models import fields
from rest_framework import serializers
from flows.models import Flow, DataFrame

class FlowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = '__all__'

class DataFrameSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataFrame
        fields = '__all__'        