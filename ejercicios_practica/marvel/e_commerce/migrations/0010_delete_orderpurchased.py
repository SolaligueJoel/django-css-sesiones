# Generated by Django 3.2.2 on 2022-06-27 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0009_auto_20220627_0348'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderPurchased',
        ),
    ]