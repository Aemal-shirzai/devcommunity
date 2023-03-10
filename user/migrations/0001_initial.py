# Generated by Django 4.1.5 on 2023-01-26 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('short_intro', models.CharField(max_length=250)),
                ('bio', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=250, null=True)),
                ('profile_image', models.ImageField(blank=True, default='default_profile.png', null=True, upload_to='profiles')),
                ('social_github', models.CharField(blank=True, max_length=500, null=True)),
                ('social_twitter', models.CharField(blank=True, max_length=500, null=True)),
                ('social_linkedin', models.CharField(blank=True, max_length=500, null=True)),
                ('social_stackoverflow', models.CharField(blank=True, max_length=500, null=True)),
                ('social_youtube', models.CharField(blank=True, max_length=500, null=True)),
                ('social_website', models.CharField(blank=True, max_length=500, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='user.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=240)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('subject', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='user.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='send_messages', to='user.profile')),
            ],
            options={
                'ordering': ['is_read', '-create_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='message',
            constraint=models.CheckConstraint(check=models.Q(('sender', models.F('receiver')), _negated=True), name='check_sender_reciever_same_message'),
        ),
    ]
