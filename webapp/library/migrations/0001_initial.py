# Generated by Django 4.2.11 on 2024-04-08 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('ip', models.GenericIPAddressField(default='NULL')),
                ('agent_location', models.TextField(default='NULL')),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payload', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('C', 'Command'), ('R', 'Reply')], max_length=1)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.device', to_field='username')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]