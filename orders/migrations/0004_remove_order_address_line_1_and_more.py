# Generated by Django 4.1.3 on 2022-11-28 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_order_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
    ]
