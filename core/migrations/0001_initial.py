# Generated by Django 4.0.2 on 2024-03-18 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/')),
                ('text', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
