# Generated by Django 4.2.7 on 2023-11-22 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('salary', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
    ]