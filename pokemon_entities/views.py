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
        pokemon_type__id=pokemon_id
    )
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
    pokemon_context = {
        'pokemon_id': requested_pokemon_type.id,
        'title_ru': requested_pokemon_type.title_ru,
        'title_en': requested_pokemon_type.title_en,
        'title_jp': requested_pokemon_type.title_jp,
        'description': requested_pokemon_type.description,
        'img_url':  request.build_absolute_uri(requested_pokemon_type.image.url),
    }
    if requested_pokemon_type.previous_evolution:
        pokemon_context.update(
            {
                'previous_evolution': {
                    'pokemon_id': requested_pokemon_type.previous_evolution.id,
                    'title_ru': requested_pokemon_type.previous_evolution.title_ru,
                    'title_en': requested_pokemon_type.previous_evolution.title_en,
                    'title_jp': requested_pokemon_type.previous_evolution.title_jp,
                    'description': requested_pokemon_type.previous_evolution.description,
                    'img_url': request.build_absolute_uri(requested_pokemon_type.previous_evolution.image.url),
                }
            }
        )
    if requested_pokemon_type.next_evolution:
        pokemon_context.update(
            {
                'next_evolution': {
                    'pokemon_id': requested_pokemon_type.next_evolution.id,
                    'title_ru': requested_pokemon_type.next_evolution.title_ru,
                    'title_en': requested_pokemon_type.next_evolution.title_en,
                    'title_jp': requested_pokemon_type.next_evolution.title_jp,
                    'description': requested_pokemon_type.next_evolution.description,
                    'img_url': request.build_absolute_uri(requested_pokemon_type.next_evolution.image.url),
                }
            }
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_context
    })
