# Generated by Django 3.1.3 on 2020-11-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_auto_20201120_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalinfo',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
