# Generated by Django 4.1.3 on 2022-11-25 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='final_price',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
