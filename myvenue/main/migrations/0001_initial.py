# Generated by Django 3.1.6 on 2021-02-15 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of the Venue')),
                ('email', models.CharField(max_length=255, verbose_name='Contact Email')),
                ('phone_number', models.BigIntegerField(verbose_name='Contact Phone Number')),
                ('capacity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price of Venue')),
                ('address', models.CharField(max_length=255, verbose_name='Address Line 1')),
                ('city', models.CharField(max_length=255)),
                ('street_number', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='venues/', verbose_name='Image of the venue')),
                ('events', models.TextField(verbose_name='Events that can be organized')),
                ('description', models.TextField(verbose_name='Description of the place')),
            ],
        ),
    ]
