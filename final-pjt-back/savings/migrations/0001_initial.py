# Generated by Django 3.2.18 on 2024-05-19 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SavingProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_way', models.TextField()),
                ('join_deny', models.TextField()),
                ('join_member', models.TextField()),
                ('etc_note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('save_trm', models.IntegerField(default=0)),
                ('intr_rate', models.FloatField(default=0)),
                ('intr_rate2', models.FloatField(default=0)),
                ('fin_prdt_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.savingproducts')),
            ],
        ),
    ]
