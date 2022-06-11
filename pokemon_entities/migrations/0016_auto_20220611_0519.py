# Generated by Django 3.1.14 on 2022-06-11 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_auto_20220611_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolves_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='evolves_to', to='pokemon_entities.pokemon'),
        ),
    ]
