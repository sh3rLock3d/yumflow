from django.db import models
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import User

class Flow(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="flows", on_delete=models.CASCADE, null=True)
    data = models.ForeignKey('DataFrame', blank=True ,null=True, on_delete=models.CASCADE,related_name='test',)


class DataFrame(models.Model):
    # https://pypi.org/project/django-picklefield/ 
    data = PickledObjectField()
    owner = models.ForeignKey(User, related_name="dataframes", on_delete=models.CASCADE, null=True)
    
    def info(self):
        return str(self.data)

