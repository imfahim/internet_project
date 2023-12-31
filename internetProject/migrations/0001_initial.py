# Generated by Django 4.2.6 on 2023-11-27 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('icon_url', models.URLField()),
                ('tier', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('price', models.FloatField()),
                ('btc_price', models.FloatField()),
                ('price_at', models.DateTimeField()),
                ('number_of_markets', models.IntegerField()),
                ('number_of_exchanges', models.IntegerField()),
                ('volume_24h', models.FloatField()),
                ('market_cap', models.FloatField()),
                ('fully_diluted_market_cap', models.FloatField()),
                ('change', models.FloatField()),
                ('all_time_high_price', models.FloatField()),
                ('all_time_high_timestamp', models.DateTimeField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('website_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='complaint_attachments/')),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Currency_rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_currency', models.CharField(max_length=3)),
                ('to_currency', models.CharField(max_length=3)),
                ('rate', models.FloatField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_proof_path', models.FileField(blank=True, null=True, upload_to='id_proofs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField()),
                ('email_address', models.EmailField(max_length=254)),
                ('payer_id', models.CharField(max_length=255)),
                ('reference_id', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency_code', models.CharField(max_length=3)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoStateData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('data', models.JSONField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': {('type',)},
            },
        ),
        migrations.CreateModel(
            name='CryptoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.IntegerField()),
                ('offset', models.IntegerField()),
                ('data', models.JSONField()),
                ('total_items', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': {('limit', 'offset')},
            },
        ),
    ]
