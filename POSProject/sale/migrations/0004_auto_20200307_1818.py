# Generated by Django 3.0.3 on 2020-03-07 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20200307_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_products',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.Order'),
        ),
    ]