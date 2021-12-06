# Generated by Django 3.2.7 on 2021-12-06 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flows', '0010_alter_modeloftrain_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='modelOfTrain',
        ),
        migrations.RemoveField(
            model_name='flow',
            name='preparation',
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testResult', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModelResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('modelOfTrain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modelOfTrain', to='flows.modeloftrain')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modelResult', to=settings.AUTH_USER_MODEL)),
                ('preparation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='train_query', to='flows.preparedata')),
                ('testResult', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testResult', to='flows.testresult')),
            ],
        ),
        migrations.AddField(
            model_name='flow',
            name='modelResult',
            field=models.ManyToManyField(blank=True, to='flows.ModelResult'),
        ),
    ]
