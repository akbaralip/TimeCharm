# Generated by Django 4.2.3 on 2023-08-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_rename_discount_percentage_productvariant_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='store_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]