# Generated by Django 3.2.5 on 2021-10-06 08:19

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Final_product_Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subID', models.IntegerField(blank=True)),
                ('totalWeight', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('date', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'Final_product_Main',
            },
        ),
        migrations.CreateModel(
            name='TeaGrades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaGrade', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'db_table': 'tea_grade',
            },
        ),
        migrations.CreateModel(
            name='Final_product_sub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subID', models.IntegerField(blank=True)),
                ('gradeWeight', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('teaGrade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.teagrades')),
            ],
            options={
                'db_table': 'Final_product_sub',
            },
        ),
    ]