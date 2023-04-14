# Generated by Django 4.1.3 on 2022-11-26 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=2000)),
                ('paragraph_1', models.CharField(max_length=20000)),
                ('paragraph_2', models.CharField(blank=True, max_length=20000)),
                ('paragraph_3', models.CharField(blank=True, max_length=20000)),
                ('paragraph_4', models.CharField(blank=True, max_length=20000)),
                ('author', models.CharField(blank=True, max_length=50)),
                ('image_1', models.ImageField(upload_to='photos/articles')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('last_modified_date', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
