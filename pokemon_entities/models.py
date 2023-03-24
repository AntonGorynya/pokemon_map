from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True,  primary_key=True)
    title_ru = models.CharField('Название на русском', max_length=200, default='Имя покемона', unique=True)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    description = models.TextField(default='Описание покемона')
    next_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='previous',
        null=True, blank=True,
        verbose_name='Следующая эволюция'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='next',
        null=True, blank=True,
        verbose_name='Предыдущая эволюция'
    )
    image = models.ImageField('Изображение', upload_to='pokemons', default='pokemons/default.png')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon_type = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=5, verbose_name='Покемон')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долготота')
    appeared_at = models.DateTimeField('Время появления', null=True)
    disappeared_at = models.DateTimeField('Время исчезания', null=True)
    level = models.IntegerField('Уровень', default=1)
    health = models.IntegerField('Здоровье', default=1)
    strength = models.IntegerField('Сила', default=0)
    defence = models.IntegerField('Защита', default=0)
    stamina = models.IntegerField('Стамина', default=0)

    def __str__(self):
        return f'{self.pokemon_type} {self.lat} {self.lon}'