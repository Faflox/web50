# Generated by Django 5.0.3 on 2024-04-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_user_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePicture',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
