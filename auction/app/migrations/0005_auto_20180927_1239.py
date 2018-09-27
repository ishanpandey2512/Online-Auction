# Generated by Django 2.1.1 on 2018-09-27 07:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180927_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visaNum', models.CharField(max_length=16)),
                ('expDate', models.DateField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MyProfile')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 28, 7, 9, 52, 63524, tzinfo=utc)),
        ),
    ]