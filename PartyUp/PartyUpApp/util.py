import re
from weakref import ref

from .models import User, SpotifyToken, Vendor
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from requests import post

import base64

def get_user_tokens(username):
    user_id = User.objects.filter(username=username)
    user_tokens = SpotifyToken.objects.filter(user=user_id[0])
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_or_create_user_tokens(username, access_token, token_type, expires_in, refresh_token):
    user_id = User.objects.filter(username=username)
    expiry = timezone.now() + timedelta(seconds=expires_in)
    obj, created = SpotifyToken.objects.update_or_create(user=user_id[0], defaults={
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': token_type,
        'expires_in': expiry
    })

def is_spotify_authenticated(username):
    tokens = get_user_tokens(username)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(username)
        return True
    return False

def refresh_spotify_token(username):
    refresh_token = get_user_tokens(username).refresh_token

    sample_string = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}'
    sample_string_bytes = sample_string.encode("ascii")
  
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    response = post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {base64_string}', 'Content-Type': 'application/x-www-form-urlencoded'}, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    if response.get('refresh_token'):
        refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(username, access_token, token_type, expires_in, refresh_token)