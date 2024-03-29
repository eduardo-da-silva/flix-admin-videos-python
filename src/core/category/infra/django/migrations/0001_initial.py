# Generated by Django 4.0.4 on 2022-07-20 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField()),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'categories',
            },
        ),
    ]
