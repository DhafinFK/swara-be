# Generated by Django 5.0.6 on 2024-07-11 19:32

import angkat_isu.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angkat_isu', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=angkat_isu.models.upload_to_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angkat_isu.post')),
            ],
        ),
    ]
