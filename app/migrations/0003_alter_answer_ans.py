# Generated by Django 4.0.1 on 2022-03-14 10:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='ans',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
