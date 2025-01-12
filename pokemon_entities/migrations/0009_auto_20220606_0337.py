# Generated by Django 3.1.14 on 2022-06-06 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20220605_0449'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolves_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ev_from', to='pokemon_entities.pokemon'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='evolves_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_to', to='pokemon_entities.pokemon'),
        ),
    ]
