# Generated by Django 3.2.7 on 2021-10-17 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0003_auto_20211005_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='x_test',
        ),
        migrations.RemoveField(
            model_name='flow',
            name='x_train',
        ),
        migrations.RemoveField(
            model_name='flow',
            name='y_test',
        ),
        migrations.RemoveField(
            model_name='flow',
            name='y_train',
        ),
        migrations.AddField(
            model_name='flow',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='flows.dataframe'),
        ),
    ]
