# Generated by Django 4.0.5 on 2022-09-20 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_costumer_delete_musician'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Costumer',
            new_name='CostumerDetail',
        ),
    ]
