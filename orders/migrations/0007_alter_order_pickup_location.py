# Generated by Django 4.1.3 on 2022-11-28 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_pickup_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pickup_location',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
