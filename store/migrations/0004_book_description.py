# Generated by Django 2.2.7 on 2019-12-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20191224_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
