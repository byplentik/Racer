# Generated by Django 4.0 on 2023-06-29 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='MainPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Основная запчасть')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='№')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('main_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.mainpart', verbose_name='Основная запчасть')),
            ],
        ),
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Мото/Двигатели')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.category', verbose_name='Категория')),
            ],
        ),
        migrations.AddField(
            model_name='mainpart',
            name='motorcycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.motorcycle', verbose_name='Мото/Двигатель'),
        ),
    ]
