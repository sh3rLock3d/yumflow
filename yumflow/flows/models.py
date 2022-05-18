from django.db import models
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Flow(models.Model):
    title = models.CharField(max_length=100,)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="flows", on_delete=models.CASCADE, null=True)
    data = models.ForeignKey('DataFrame', blank=True ,null=True, on_delete=models.CASCADE,related_name='train',)
    dataTest = models.ForeignKey('DataFrame', blank=True ,null=True, on_delete=models.CASCADE,related_name='test',)
    modelResult = models.ManyToManyField('ModelResult', blank=True)



class DataFrame(models.Model):
    # https://pypi.org/project/django-picklefield/ 
    data = PickledObjectField()
    owner = models.ForeignKey(User, related_name="dataframes", on_delete=models.CASCADE, null=True)
    
    def info(self):
        return str(self.data)

class ModelResult(models.Model):
    name = models.CharField(max_length=100, unique=True)
    preparation = models.ForeignKey('PrepareData', blank=True ,null=True, on_delete=models.CASCADE,related_name='train_query',)
    hyperparameters = PickledObjectField(blank=True ,null=True)
    modelOfTrain = models.ForeignKey('ModelOfTrain', blank=True ,null=True, on_delete=models.CASCADE,related_name='modelOfTrain',)
    testResult = models.ForeignKey('TestResult', blank=True ,null=True, on_delete=models.CASCADE,related_name='testResult',)
    owner = models.ForeignKey(User, related_name="modelResult", on_delete=models.CASCADE, null=True)


class PrepareData(models.Model):
    cols = PickledObjectField()
    nans = PickledObjectField()
    categories = PickledObjectField()
    normalize = PickledObjectField()
    sliceStr=PickledObjectField()
    colFilter = models.IntegerField(blank=True, null=True)
    constraints = models.CharField(max_length=100,)
    owner = models.ForeignKey(User, related_name="prepareData", on_delete=models.CASCADE, null=True)


def user_directory_path(instance, filename):
    return 'uploads/1.tzt'

class ModelOfTrain(models.Model):
    owner = models.ForeignKey(User, related_name="modelOfTrain", on_delete=models.CASCADE, null=True)
    upload = models.FileField(upload_to='uploads/')
    

class TestResult(models.Model):
    owner = models.ForeignKey(User, related_name="testResult", on_delete=models.CASCADE, null=True)
    score = models.FloatField(default=-1.0)
