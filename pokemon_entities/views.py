import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core import exceptions

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_evolution_serialized(pokemon: Pokemon, request):
    if pokemon is None:
        return None

    pokemon_image_uri = None

    if pokemon.image:
        pokemon_image_uri = request.build_absolute_uri(pokemon.image.url)

    pokemon_serialized = {
        "title_ru": pokemon.title,
        "pokemon_id": pokemon.id,
        "img_url": pokemon_image_uri
    }

    return pokemon_serialized


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
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()
    pokemon_image_uris = {}

    for pokemon in pokemons:
        pokemon_image_uris[pokemon.title] = request.build_absolute_uri(pokemon.image.url) if pokemon.image else None

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        pokemon_image_uri = pokemon_image_uris[pokemon.title]
        if pokemon_image_uri:
            for pokemon_entity in pokemon_entities:
                if pokemon_entity.is_available():
                    add_pokemon(
                        folium_map, pokemon_entity.lat,
                        pokemon_entity.lon,
                        pokemon_image_uri
                    )


    pokemons_on_page = []

    for pokemon in pokemons:
        pokemon_image_uri = pokemon_image_uris[pokemon.title]
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_uri,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except exceptions.ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    next_evolutions = Pokemon.objects.filter(evolves_from_id=requested_pokemon.id)

    if not next_evolutions:
        next_evolutions = [None]

    previous_evolution = requested_pokemon.evolves_from

    requested_pokemon_image_uri = None

    if requested_pokemon.image:
        requested_pokemon_image_uri = request.build_absolute_uri(requested_pokemon.image.url)

    requested_pokemon_serialized = {
        "pokemon_id": pokemon_id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": requested_pokemon_image_uri,
        "next_evolution": get_evolution_serialized(next_evolutions[0], request),
        "previous_evolution": get_evolution_serialized(previous_evolution, request)
    }

    pokemon_entities = PokemonEntity.objects.filter(pokemon_id=int(pokemon_id))
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon_image_uri
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon_serialized
    })
