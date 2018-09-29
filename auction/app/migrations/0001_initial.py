# Generated by Django 2.1.1 on 2018-09-29 15:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('bidder_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=10, null=True)),
                ('avatar', models.ImageField(default='profile.png', upload_to='profile_pic')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desp', models.TextField(max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='../static/images/')),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('minimum_price', models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateTimeField(default=datetime.datetime(2018, 9, 30, 15, 33, 17, 767267, tzinfo=utc))),
                ('current_bid', models.IntegerField(default=0)),
                ('product_sold', models.BooleanField(default=False)),
                ('seller_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visaNum', models.CharField(max_length=16)),
                ('expDate', models.DateField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MyProfile')),
            ],
        ),
        migrations.AddField(
            model_name='bids',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]
