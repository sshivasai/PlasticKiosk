# Generated by Django 4.1.3 on 2022-11-28 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_cat_id'),
        ('orders', '0007_alter_order_pickup_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_location',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
