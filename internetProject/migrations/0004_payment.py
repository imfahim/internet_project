# Generated by Django 4.2.6 on 2023-11-26 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internetProject', '0003_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField()),
                ('given_name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=254)),
                ('payer_id', models.CharField(max_length=255)),
                ('reference_id', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency_code', models.CharField(max_length=3)),
            ],
        ),
    ]
