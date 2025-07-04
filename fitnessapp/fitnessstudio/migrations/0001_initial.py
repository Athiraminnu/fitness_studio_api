# Generated by Django 5.2.3 on 2025-06-20 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('time', models.TimeField()),
                ('available_slots', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Instructor_name', models.CharField(max_length=100)),
                ('class_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitnessstudio.class')),
            ],
        ),
    ]
