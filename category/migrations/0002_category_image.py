# Generated by Django 4.1.3 on 2022-11-27 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='photos/category'),
            preserve_default=False,
        ),
    ]
