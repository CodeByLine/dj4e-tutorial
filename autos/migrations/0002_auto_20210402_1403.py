# Generated by Django 3.1.7 on 2021-04-02 19:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='nickname',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Nickname must be greater than 1 character')]),
        ),
        migrations.AlterField(
            model_name='make',
            name='name',
            field=models.CharField(help_text='Enter a make (e.g. Dodge)', max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Make must be greater than 1 character')]),
        ),
    ]
