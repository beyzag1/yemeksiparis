# Generated by Django 5.0.3 on 2024-05-29 10:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yemekke', '0002_orderitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RestoranUser',
            new_name='SellerUser',
        ),
        migrations.RenameModel(
            old_name='CustomerUser',
            new_name='User',
        ),
    ]
