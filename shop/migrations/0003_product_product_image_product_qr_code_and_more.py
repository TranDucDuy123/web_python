# Generated by Django 5.1.1 on 2024-09-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_bill_id_alter_billitems_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AddField(
            model_name='product',
            name='qr_code2',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
