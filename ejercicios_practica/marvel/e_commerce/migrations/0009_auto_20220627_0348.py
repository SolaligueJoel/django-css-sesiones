# Generated by Django 3.2.2 on 2022-06-27 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('e_commerce', '0008_orderpurchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpurchased',
            name='comic_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='e_commerce.comic', verbose_name='Comic'),
        ),
        migrations.AlterField(
            model_name='orderpurchased',
            name='comic_qty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_commerce.wishlist', verbose_name='comic qty'),
        ),
        migrations.AlterField(
            model_name='orderpurchased',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
