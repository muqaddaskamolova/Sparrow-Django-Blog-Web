# Generated by Django 4.1.6 on 2023-02-13 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=40, verbose_name='Developer`s name')),
                ('job', models.CharField(max_length=30, verbose_name='Job')),
                ('bio', models.TextField(verbose_name='About me')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/developers')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Developer',
            },
        ),
    ]
