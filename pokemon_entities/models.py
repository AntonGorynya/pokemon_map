from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True,  primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='pokemons', default='pokemons/default.png')

    def __str__(self):
        return self.title


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