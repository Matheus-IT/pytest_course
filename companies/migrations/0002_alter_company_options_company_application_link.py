# Generated by Django 4.0.5 on 2022-06-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='company',
            name='application_link',
            field=models.URLField(blank=True),
        ),
    ]