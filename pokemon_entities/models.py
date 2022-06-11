from django.db import models  # noqa F401
import django.utils.timezone as timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='Об этом покемоне нам пока ничего не известно :(', blank=True)
    evolves_from = models.ForeignKey(to='self',
                                     on_delete=models.RESTRICT,
                                     related_name='evolves_to',
                                     null=True,
                                     blank=True)

    class Meta:
        verbose_name = 'pokemon'

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(to=Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)

    level = models.IntegerField(default=0)
    health = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    defence = models.IntegerField(blank=True, null=True)
    stamina = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'pokemon entity'

    def __str__(self):
        return f'{self.pokemon.title} {self.level} lvl.'

    def is_available(self) -> bool:
        appeared_at_local = timezone.localtime(self.appeared_at)
        disappeared_at_local = timezone.localtime(self.disappeared_at)

        availability = appeared_at_local > timezone.now() or disappeared_at_local < timezone.now()

        return availability
