# Generated by Django 5.1.3 on 2024-12-01 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('farmers', '0002_product_delete_produce'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='products_owned', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_uploaded',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
