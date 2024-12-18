# Generated by Django 5.0.6 on 2024-05-24 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_uloga_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uloga',
            name='role',
            field=models.CharField(choices=[('Professor', 'profesor'), ('Student', 'student'), ('Admin', 'admin')], default='admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='upisi',
            name='status',
            field=models.CharField(choices=[('P', 'Polozeno'), ('N', 'Nepolozeno'), ('U', 'Upisano'), ('PU', 'PONOVNO UPISANO')], default='U', max_length=65),
        ),
    ]
