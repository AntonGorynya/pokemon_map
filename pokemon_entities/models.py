from django.db import models  # noqa F401


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True,  primary_key=True)
    title_ru = models.CharField('Название на русском', max_length=200, default='Имя покемона', unique=True)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    description = models.TextField(default='Описание покемона')
    next_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET(None),
        related_name='prev_evolutions',
        null=True,
        blank=True,
        verbose_name='Следующая эволюция'
    )
    image = models.ImageField('Изображение', upload_to='pokemons', default='pokemons/default.png')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    ptype = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Время исчезания', null=True, blank=True)
    level = models.IntegerField('Уровень', default=0)
    health = models.IntegerField('Здоровье', default=0)
    strength = models.IntegerField('Сила', default=0)
    defence = models.IntegerField('Защита', default=0)
    stamina = models.IntegerField('Стамина', default=0)

    def __str__(self):
        return f'{self.ptype.title_ru} {self.lat} {self.lon}'
