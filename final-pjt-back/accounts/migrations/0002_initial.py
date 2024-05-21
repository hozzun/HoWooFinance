# Generated by Django 4.2.8 on 2024-05-21 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deposits', '0001_initial'),
        ('accounts', '0001_initial'),
        ('savings', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deposit',
            field=models.ManyToManyField(blank=True, related_name='deposit_joined', to='deposits.depositproducts'),
        ),
        migrations.AddField(
            model_name='user',
            name='deposit_options',
            field=models.ManyToManyField(blank=True, related_name='user_deposit_options', to='deposits.depositoptions'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='saving',
            field=models.ManyToManyField(blank=True, related_name='saving_joined', to='savings.savingproducts'),
        ),
        migrations.AddField(
            model_name='user',
            name='saving_options',
            field=models.ManyToManyField(blank=True, related_name='users_saving_options', to='savings.savingoptions'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]