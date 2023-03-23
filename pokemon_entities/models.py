from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True,  primary_key=True)
    title_ru = models.CharField('Название на русском', max_length=200)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    description = models.TextField(default='Описание покемона')
    next_evolution = models.IntegerField('ID В кого эволюционирует ', null=True)
    previous_evolution = models.IntegerField('ID Из В кого эволюционирует', null=True)
    image = models.ImageField(upload_to='pokemons', default='pokemons/default.png')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon_type = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=5)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)