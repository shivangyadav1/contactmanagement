# Generated by Django 4.0.4 on 2022-04-26 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
