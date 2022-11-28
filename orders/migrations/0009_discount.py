# Generated by Django 4.1.3 on 2022-11-27 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('stripe_id', models.CharField(max_length=55)),
                ('promocode', models.CharField(max_length=55)),
                ('percent_off', models.IntegerField(max_length=3)),
                ('active', models.BooleanField(default=True)),
                ('visible_in_checkout', models.BooleanField(default=True)),
            ],
        ),
    ]