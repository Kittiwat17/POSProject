# Generated by Django 3.0.3 on 2020-03-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]