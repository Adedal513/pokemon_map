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
                                     related_name='previous_evolutions',
                                     null=True,
                                     blank=True,
                                     default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'pokemon'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(to=Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)

    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0, blank=True, null=True)
    strength = models.IntegerField(default=0, blank=True, null=True)
    defence = models.IntegerField(default=0, blank=True, null=True)
    stamina = models.IntegerField(default=0, blank=True, null=True)

    def is_available(self):
        appeared_at_local = timezone.localtime(self.appeared_at)
        disappeared_at_local = timezone.localtime(self.disappeared_at)

        if appeared_at_local > timezone.now() or disappeared_at_local < timezone.now():
            return False

        return True

    def __str__(self):
        return f'{self.pokemon.title} {self.level} lvl.'

    class Meta:
        verbose_name = 'pokemon entity'
