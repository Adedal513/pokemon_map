from django.db import models  # noqa F401
import django.utils.timezone as timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    evolves_from = models.ForeignKey(to='self', on_delete=models.RESTRICT, related_name='ev_from', null=True, blank=True, default=None)
    evolves_to = models.ForeignKey(to='self', on_delete=models.CASCADE, related_name='ev_to', null=True, blank=True, default=None)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(to=Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)

    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def is_available(self):
        appeared_at_local = timezone.localtime(self.appeared_at)
        disappeared_at_local = timezone.localtime(self.disappeared_at)

        if appeared_at_local > timezone.now() or disappeared_at_local < timezone.now():
            return False

        return True

    def __str__(self):
        return f'{self.pokemon.title} {self.level} lvl.'
