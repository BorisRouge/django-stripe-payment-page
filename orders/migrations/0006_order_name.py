# Generated by Django 4.1.3 on 2022-11-27 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_delete_discount_delete_tax_remove_order_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=55, null=True),
        ),
    ]
