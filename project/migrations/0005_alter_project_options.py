# Generated by Django 4.1.4 on 2023-01-17 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-create_date', 'title']},
        ),
    ]