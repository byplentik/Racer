# Generated by Django 4.0 on 2024-02-08 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basket', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specifieddeliveryaddressmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='part',
            name='main_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.mainpart', verbose_name='Основная запчасть'),
        ),
        migrations.AddField(
            model_name='orderedpart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_parts', to='basket.checkoutcart', verbose_name='Оформленный заказ'),
        ),
        migrations.AddField(
            model_name='orderedpart',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.part', verbose_name='Запчасть'),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='mainpart',
            name='motorcycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.motorcycle', verbose_name='Мото/Двигатель'),
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_method', to='basket.checkoutcart'),
        ),
        migrations.AddField(
            model_name='commentadministratorforcheckoutcart',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basket.checkoutcart'),
        ),
        migrations.AddField(
            model_name='checkoutcart',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basket.specifieddeliveryaddressmodel', verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='checkoutcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='additionalitemtocheckoutcart',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='additional_item', to='basket.checkoutcart'),
        ),
    ]