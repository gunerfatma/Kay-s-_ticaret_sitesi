# Generated by Django 4.2 on 2023-07-18 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urunler',
            old_name='Category',
            new_name='category',
        ),
    ]