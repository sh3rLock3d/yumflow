# Generated by Django 3.2.7 on 2022-05-16 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0018_alter_modelresult_hyperparameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='flow',
            name='dataTest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='flows.dataframe'),
        ),
    ]
