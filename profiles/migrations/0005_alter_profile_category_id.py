# Generated by Django 4.0.6 on 2022-08-16 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='category_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
