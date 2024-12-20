# Generated by Django 5.1.3 on 2024-12-06 21:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('farmers', '0010_message_product_is_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
