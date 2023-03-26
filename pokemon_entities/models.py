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
        related_name='prev_evolutions',
        null=True,
        blank=True,
        verbose_name='Следующая эволюция'
    )
    image = models.ImageField('Изображение', upload_to='pokemons', null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Время исчезания', null=True, blank=True)
    level = models.IntegerField('Уровень', null=True)
    health = models.IntegerField('Здоровье', null=True)
    strength = models.IntegerField('Сила', null=True)
    defence = models.IntegerField('Защита', null=True)
    stamina = models.IntegerField('Стамина', null=True)

    def __str__(self):
        return f'{self.pokemon.title_ru} {self.lat} {self.lon}'
