# Generated by Django 3.1.14 on 2022-06-02 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
