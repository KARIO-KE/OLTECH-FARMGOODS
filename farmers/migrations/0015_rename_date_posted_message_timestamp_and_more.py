# Generated by Django 5.1.3 on 2024-12-08 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('farmers', '0014_alter_product_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date_posted',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='message',
            name='short_message',
            field=models.TextField(),
        ),
    ]