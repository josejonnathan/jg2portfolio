# Generated by Django 4.2.15 on 2024-08-28 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0007_alter_skill_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
