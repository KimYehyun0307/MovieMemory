# Generated by Django 4.2.16 on 2024-11-20 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField(blank=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
