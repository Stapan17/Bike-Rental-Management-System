# Generated by Django 3.1.4 on 2021-06-30 13:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('bike_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('bike_color', models.CharField(choices=[('Red', 'Red'), ('White', 'White'), ('Black', 'Black'), ('Blue', 'Blue')], max_length=20)),
                ('bike_type', models.CharField(choices=[('Regular', 'Regular'), ('Non Gear', 'Non Gear'), ('Sports', 'Sports')], max_length=20)),
                ('bike_model', models.CharField(max_length=30)),
                ('bike_brand', models.CharField(max_length=30)),
                ('bike_available', models.CharField(choices=[('Available', 'Available'), ('Not Available', 'Not Available')], max_length=20)),
                ('bike_user', models.CharField(blank=True, default='NONE', max_length=30)),
                ('bike_rent_number', models.PositiveIntegerField(blank=True, default=1)),
                ('bike_rent', models.CharField(blank=True, max_length=30)),
                ('date_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='contactUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=50)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('Transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('Payment_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('Payment_user', models.CharField(max_length=20)),
                ('Payment_station', models.CharField(max_length=20)),
                ('Payment_bike_number', models.CharField(max_length=10)),
                ('Payment_bike_color', models.CharField(max_length=20)),
                ('Payment_bike_type', models.CharField(max_length=20)),
                ('Payment_bike_model', models.CharField(max_length=30)),
                ('Payment_bike_brand', models.CharField(max_length=30)),
                ('Payment_rent_type', models.CharField(max_length=30)),
                ('Payment_rent_number', models.CharField(max_length=30)),
                ('Payment_emp_name', models.CharField(blank=True, default='Employee Name', max_length=30)),
                ('Payment_bill_amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.AutoField(primary_key=True, serialize=False)),
                ('station_address', models.CharField(max_length=50)),
                ('station_phoneNo', models.CharField(max_length=10)),
                ('bike_quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='userProof',
            fields=[
                ('Adhar_card', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('driving_licence', models.CharField(max_length=12)),
                ('passport_No', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=12)),
                ('proof_of_user', models.CharField(max_length=20)),
                ('user_bike', models.CharField(blank=True, default='NOT TAKEN', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourly_rent', models.PositiveIntegerField()),
                ('daily_rent', models.PositiveIntegerField()),
                ('weekly_rent', models.PositiveIntegerField()),
                ('hourly_penalty', models.PositiveIntegerField()),
                ('daily_penalty', models.PositiveIntegerField()),
                ('weekly_penalty', models.PositiveIntegerField()),
                ('bike_rent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appBRS.bike')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_name', models.CharField(max_length=30)),
                ('employee_phonNo', models.CharField(max_length=10)),
                ('employee_superkey', models.CharField(max_length=20)),
                ('station_emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBRS.station')),
            ],
        ),
        migrations.AddField(
            model_name='bike',
            name='bike_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBRS.station'),
        ),
    ]
