from django.db import models
from django.db.models import fields
from rest_framework import serializers
from flows.models import Flow, DataFrame, PrepareData, ModelOfTrain
from rest_framework.validators import UniqueTogetherValidator

class FlowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = '__all__'
        '''
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['owner', 'title'],
            )
        ]
        '''
        

class DataFrameSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataFrame
        fields = '__all__'        

class PrepareDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataFrame
        fields = '__all__' 

class ModelOfTrainSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModelOfTrain
        fields = '__all__' 