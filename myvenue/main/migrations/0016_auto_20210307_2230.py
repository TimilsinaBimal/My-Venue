# Generated by Django 3.1.7 on 2021-03-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_order_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name='Ordered Date and Time'),
        ),
    ]
