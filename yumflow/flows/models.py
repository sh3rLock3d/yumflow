from django.db import models

from django.db import models
from picklefield.fields import PickledObjectField

class Flow(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    x_test = models.ForeignKey('DataFrame', blank=True ,null=True, on_delete=models.CASCADE,related_name='x_test',)
    y_test = models.ForeignKey('DataFrame', blank=True, null=True, on_delete=models.CASCADE,related_name='y_test',)
    x_train = models.ForeignKey('DataFrame', blank=True, null=True, on_delete=models.CASCADE,related_name='x_train',)
    y_train = models.ForeignKey('DataFrame', blank=True, null=True, on_delete=models.CASCADE,related_name='y_train',)

class DataFrame(models.Model):
    # https://pypi.org/project/django-picklefield/ 
    data = PickledObjectField()


    def info(self):
        return str(self.data)
