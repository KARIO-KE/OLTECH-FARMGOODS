# Generated by Django 5.1.3 on 2024-12-03 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0004_alter_product_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='roduct_type',
            field=models.CharField(default='100', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name='product',
            name='farmer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farmers.farmer'),
        ),
    ]
