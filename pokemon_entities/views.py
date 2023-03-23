import folium
import json
import datetime

from django.utils import timezone
from pokemon_entities.models import PokemonEntity, Pokemon
from django.http import HttpRequest
from django.http import HttpResponseNotFound
from django.shortcuts import render


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    today = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lt=today, disappeared_at__gt=today)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        url = None
        if pokemon.pokemon_type.image.path:
            url = pokemon.pokemon_type.image.path
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            url
        )
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.image.url:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title_ru,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    today = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(
        appeared_at__lt=today,
        disappeared_at__gt=today,
        pokemon_type__id=pokemon_id)

    if not pokemons:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon_type = Pokemon.objects.get(id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        url = pokemon.pokemon_type.image.path
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            url
        )




    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon_type
    })

'''
{'pokemon_id': 2,
 'title_ru': 'Ивизавр',
 'title_en': 'Ivysaur',
 'title_jp': 'フシギソウ',
 'description': 'покемон двойного травяного и ядовитого типа из первого поколения покемонов. Эволюционирует из стартового покемона Бульбазавра на 16 уровне. С
тановится Венузавром на 32 уровне.',
 'img_url': 'https://vignette.wikia.nocookie.net/pokemon/images/7/73/002Ivysaur.png/revision/latest/scale-to-width-down/200?cb=20150703180624&path-prefix=ru', 
 'entities': [{'level': 44, 'lat': 55.729472, 'lon': 3
7.692479}, {'level': 24, 'lat': 55.730141, 'lon': 37.653911}], 
'next_evolution': {'title_ru': 'Венузавр', 'pokemon_id': 3, 'img_url': 'https://vignette.wikia.nocookie.net/pokemon/images/a/ae/003Venusaur.png/revision/latest/scale-to-width-down/200?c
b=20150703175822&path-prefix=ru'}, 
'previous_evolution': {'title_ru': 'Бульбазавр', 'pokemon_id': 1, 'img_url': 'https://upload.wikimedia.org/wikipedia/ru/c/ca/%D0%91%D1%83%D0%BB%D1%8C%D0%B1%D0%B0%D0%B7%D0%B0%D0%B2%D1%80.png'}}


'''