# Generated by Django 5.0.6 on 2024-05-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_predmet_izborni_predmet_sem_izv_predmet_sem_red'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uloga',
            name='name',
        ),
        migrations.AddField(
            model_name='uloga',
            name='role',
            field=models.CharField(choices=[('prof', 'profesor'), ('stu', 'student'), ('adm', 'admin')], default='adm', max_length=50),
        ),
    ]
