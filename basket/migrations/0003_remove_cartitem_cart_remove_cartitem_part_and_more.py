# Generated by Django 4.0 on 2023-08-06 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='part',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]