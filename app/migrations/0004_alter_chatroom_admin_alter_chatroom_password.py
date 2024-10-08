# Generated by Django 4.2.3 on 2024-08-05 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_chatroom_admin_chatroom_password_alter_chatroom_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
