# Generated by Django 4.1.6 on 2023-02-03 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_alter_post_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
