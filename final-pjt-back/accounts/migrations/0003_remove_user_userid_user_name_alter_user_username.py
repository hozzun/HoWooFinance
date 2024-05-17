# Generated by Django 4.2.8 on 2024-05-17 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_userid_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userid',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='unKnown', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
