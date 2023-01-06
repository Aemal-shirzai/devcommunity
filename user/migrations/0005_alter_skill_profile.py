# Generated by Django 4.1.4 on 2023-01-06 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_skill_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='user.profile'),
        ),
    ]
