# Generated by Django 4.1.3 on 2022-11-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]