# Generated by Django 4.0.5 on 2022-09-20 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_costumer_costumerdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costumerdetail',
            name='state',
        ),
    ]