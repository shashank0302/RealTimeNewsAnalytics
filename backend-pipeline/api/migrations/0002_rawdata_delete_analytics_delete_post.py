# Generated by Django 5.1.7 on 2025-04-02 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('sentiment_score', models.FloatField(blank=True, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Analytics',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
