# Generated by Django 5.1.3 on 2024-12-06 22:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0003_alter_product_farmer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
