# Generated by Django 3.1.2 on 2021-01-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210117_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
