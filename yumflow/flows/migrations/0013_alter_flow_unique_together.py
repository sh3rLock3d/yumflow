# Generated by Django 3.2.7 on 2021-12-13 08:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flows', '0012_alter_flow_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flow',
            unique_together={('title', 'owner')},
        ),
    ]
