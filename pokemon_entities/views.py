import folium

from django.utils import timezone
from pokemon_entities.models import PokemonEntity, Pokemon
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.shortcuts import render


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_url(path):
    if path:
        return path
    return None

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
    pokemons_entities = PokemonEntity.objects.filter(appeared_at__lt=today, disappeared_at__gt=today)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemons_entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            get_url(entity.ptype.image.path)
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
    requested_pokemon_type = get_object_or_404(Pokemon, id=pokemon_id)

    today = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(
        appeared_at__lt=today,
        disappeared_at__gt=today,
        ptype__id=pokemon_id
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            get_url(pokemon.ptype.image.path)
        )
    serialized_pokemon = {
        'pokemon_id': requested_pokemon_type.id,
        'title_ru': requested_pokemon_type.title_ru,
        'title_en': requested_pokemon_type.title_en,
        'title_jp': requested_pokemon_type.title_jp,
        'description': requested_pokemon_type.description,
        'img_url':  request.build_absolute_uri(requested_pokemon_type.image.url),
    }
    previous_evolution = requested_pokemon_type.prev_evolutions.first()
    if previous_evolution:
        serialized_pokemon.update(
            {
                'previous_evolution': {
                    'pokemon_id': previous_evolution.id,
                    'title_ru': previous_evolution.title_ru,
                    'title_en': previous_evolution.title_en,
                    'title_jp': previous_evolution.title_jp,
                    'description': previous_evolution.description,
                    'img_url': request.build_absolute_uri(previous_evolution.image.url),
                }
            }
        )
    if requested_pokemon_type.next_evolution:
        serialized_pokemon.update(
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
        'map': folium_map._repr_html_(), 'pokemon': serialized_pokemon
    })
