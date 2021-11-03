# Generated by Django 3.2.7 on 2021-11-03 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0007_auto_20211031_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelOfTrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.AddField(
            model_name='flow',
            name='modelOfTrain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modelOfTrain', to='flows.modeloftrain'),
        ),
    ]
