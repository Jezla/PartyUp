from asyncio import constants
from distutils.log import error
from distutils.util import execute
from email import contentmanager
import enum
import http

import imp
from multiprocessing import AuthenticationError
from telnetlib import STATUS
from django.forms import models
from django.forms import ChoiceField
from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from .forms import ChoosePartneredVendorForm, PartyEventInfoForm, ChooseOwnVenueForm, ChoosePartneredVenueForm, UserSignUpForm, UserUpdateForm,VendorUpdateForm, PasswordChangeForm, PartyPlaylistForm, InviteGuestsForm, EnterChecklistForm, VendorRatingForm

from .models import Booking, Guest, Item, Transaction, User, Vendor, Event, Ratings
from django.contrib.auth import login as auth_login, authenticate, logout

from django.conf import settings

from requests import Request, post, put, get, delete

from .util import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.serializers import serialize 

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from json import dumps

import json

from datetime import datetime

from django.db import transaction

from address.models import Address


# Create your views here.

"""This method loads the initial home page 
"""
def index(request):
    context = {}
    return render(request, 'PartyUpApp/index.html', context)

"""This method loads the login page and the form inside it 
"""
def login(request):
    if request.method == 'POST': 
        # Create form with request data in it
        # First argument is if you want cookie validation support in web browser, second must be request data
        form = AuthenticationForm(None, request.POST)
        # Check all validation criteria, is_valid implemented by default via UserCreationForm
        if form.is_valid():
            # Process data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser==False:
                auth_login(request, user)
                if user.is_member:
                    return redirect('partyupapp:user_home')
                else:
                    return redirect('partyupapp:vendor_home')
            # if this is an admin logging in
            elif (user.is_superuser):
                return redirect('http://127.0.0.1:8000/admin')
        return render(request,'PartyUpApp/login.html', {'form': form})
    else:
        form = AuthenticationForm(None)
        return render(request,'PartyUpApp/login.html', {'form': form})

"""This method logs the user out
"""
def logout_view(request):
    logout(request)
    return redirect('partyupapp:home')

"""This method loads the register page and the register form
"""
def register(request):
    if settings.GOOGLE_API_KEY:
        google_api_key_set = True
    else:
        google_api_key_set = False

    if request.method == 'POST':
        # Create form with request data in it
        form = UserSignUpForm(request.POST)
        # Check all validation criteria, is_valid implemented by default via UserCreationForm
        if form.is_valid():
            # Process data
            user = form.save(commit=False)
            user.phone_number = form.cleaned_data['number'].as_national
            if form.cleaned_data['account_type'] == "Member":
                user.is_member = True
                user.save()
            else:
                user.is_vendor = True
                v_type = form.cleaned_data['vendor_type']
                if v_type == "Venue":
                    v_address = form.cleaned_data['address']
                    vendor = Vendor(user=user, type=v_type, address=v_address)
                else:
                    vendor = Vendor(user=user, type=v_type, address=None)
                user.save()
                vendor.save()
            auth_login(request, user)
            if user.is_vendor:
                return redirect('partyupapp:vendor_home')
            else:
                return redirect('partyupapp:user_home')
        return render(request,'PartyUpApp/register.html', {'form': form, 'google_api_key_set': google_api_key_set})
    else:
        form = UserSignUpForm()
        return render(request,'PartyUpApp/register.html', {'form': form, 'google_api_key_set': google_api_key_set})

"""This method loads party hub (a list of all the past and futuer events)
"""
def party_hub(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')

    if request.method == 'GET':
        events = Event.objects.filter(user_id=request.user.id).values()
        return render(request, 'PartyUpApp/party_hub.html', {'events': events})

"""This method loads user home page after login
"""
def user_home(request):
    return render(request, 'PartyUpApp/user_home.html')

"""This method loads user's events
"""
def event_page(request, event_id):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')

    if request.method == 'GET':
        if event_id > 0:
            event = Event.objects.filter(id=event_id).values()
            address = Address.objects.get(pk=event[0]['address_id'])
            if event.exists():
                return render(request, 'PartyUpApp/event_page.html', {'event': event[0], 'address': address})
            return render(request, 'PartyUpApp/party_hub.html', {'error': 'That event does not exist'})

"""This method loads vendor home page after login
"""
def vendor_home(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')

    return render(request, 'PartyUpApp/vendor_home.html')

"""This method loads About Us page
"""
def about(request):
    context = {}
    return render(request, 'PartyUpApp/about.html', context)

"""This method loads Contact Us page
"""
def contact(request):
    context = {}
    return render(request, 'PartyUpApp/contact.html', context)

def submit(request):
    context = {}
    return render(request, 'PartyUpApp/submit.html', context)

"""This method loads Privacy Policy page
"""
def policy(request):
    context = {}
    return render(request, 'PartyUpApp/privacy.html', context)

"""This method loads FAQ page
"""
def faq(request):
    context = {}
    return render(request, 'PartyUpApp/faq.html', context)

"""This method loads create_event page and its functionality
"""
def create_event(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.user.is_member:
        if request.method == 'POST':
            # Create form with request data in it
            form = PartyEventInfoForm(request.POST)
            # Check all validation criteria, is_valid implemented by default via UserCreationForm
            if form.is_valid():
                # Process data
                request.session['name'] = form.cleaned_data['name']
                request.session['description'] = form.cleaned_data['description']
                date_dict = json.loads(json.dumps({'start_date': form.cleaned_data['start_date'], 'end_date': form.cleaned_data['end_date']}, default=str))
                request.session['start_date'] = date_dict['start_date']
                request.session['end_date'] = date_dict['end_date']
                return JsonResponse({'message': 'Success'}, status=200)
            return JsonResponse({'form_errors': form.errors.as_json(escape_html=True)}, status=500)
        else:
            form = PartyEventInfoForm()
            return render(request, 'PartyUpApp/create_event.html', {'form': form})
    else:
        return redirect('partyupapp:login')


"""This method loads choose venue page and its functionality
"""
def choose_venue(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if settings.GOOGLE_API_KEY:
        google_api_key_set = True
    else:
        google_api_key_set = False
    if request.method == 'POST':
        if request.POST.get('venue_username', None):
            partnered_form = ChoosePartneredVenueForm(request.POST)
            # Check all validation criteria, is_valid implemented by default via UserCreationForm
            if partnered_form.is_valid():
                # Process data
                request.session['venue_username'] = partnered_form.cleaned_data['venue_username']
                return JsonResponse({'message': 'Success'}, status=200)
            return JsonResponse({'form_errors': partnered_form.errors.as_json(escape_html=True)}, status=500)
        else:
            own_form = ChooseOwnVenueForm(request.POST)
            if own_form.is_valid():
                # Process data
                request.session['address'] = f"{own_form.cleaned_data['address']}"
                return JsonResponse({'message': 'Success'}, status=200)
            return JsonResponse({'form_errors': own_form.errors.as_json(escape_html=True)}, status=500)
    else:
        partnered_form = ChoosePartneredVenueForm()
        own_form = ChooseOwnVenueForm()
        return render(request,'PartyUpApp/choose_venue.html', {'partnered_form': partnered_form, 'own_form': own_form, 'google_api_key_set': google_api_key_set})

"""This method loads choose vendors page and its functionality
"""
def choose_vendors(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.method == 'POST':
        if request.POST.getlist('vendor_list', None):
            vendor_list_str = request.POST.getlist('vendor_list', None)
            if vendor_list_str == ['']:
                request.session['vendor_list'] = []
                return JsonResponse({'message': 'Success'}, status=200)
            vendor_list = vendor_list_str[0].split(',')
            for username in vendor_list:
                form = ChoosePartneredVendorForm({'vendor_username': username})
                if not form.is_valid():
                    # Process data
                    return JsonResponse({'form_errors': form.errors.as_json(escape_html=True)}, status=500)
            request.session['vendor_list'] = vendor_list
            return JsonResponse({'message': 'Success'}, status=200)
    else:
        form = ChoosePartneredVendorForm()
        return render(request,'PartyUpApp/hire_vendors.html', {'form': form})

"""This method loads choose invite guests page and its functionality
"""
def invite_guest(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.method == 'POST':
        if request.POST.getlist('guest_list', None):
            guest_list_str = request.POST.getlist('guest_list')
            if guest_list_str == ['']:
                request.session['guest_list'] = []
                return JsonResponse({'message': 'Success'}, status=200)
            guest_list = guest_list_str[0].split(',')
            for username in guest_list:
                form = InviteGuestsForm({'guest_username': username})
                if not form.is_valid():
                    return JsonResponse({'form_errors': form.errors.as_json(escape_html=True)}, status=500)
            request.session['guest_list'] = guest_list
            return JsonResponse({'message': 'Success'}, status=200)
    else:
        form = InviteGuestsForm()
        return render(request,'PartyUpApp/invite_guest.html', {'form': form})

"""This method loads checklist page and its functionality
"""
def checklist(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.method == 'POST':
        # Process data
        if request.POST.getlist('item_list', None):
            items_list_str = request.POST.getlist('item_list', None)
            if items_list_str == ['']:
                request.session['item_list'] = []
                return JsonResponse({'message': 'Success'}, status=200)
            items_list = items_list_str[0].split(',')
            for item in items_list:
                form = EnterChecklistForm({'name': item})
                if not form.is_valid():
                    return JsonResponse({'form_errors': form.errors.as_json(escape_html=True)}, status=500)
            request.session['item_list'] = items_list
            return JsonResponse({'message': 'Success'}, status=200)        
    else:
        form = EnterChecklistForm()
        return render(request, 'PartyUpApp/checklist.html', {'form': form})

"""This method loads spotify authentication page when creating playlists
"""
def spotifyAuthURL(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.method == 'GET':
        scopes = 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email user-read-private'
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes, 
            'response_type': 'code',
            'redirect_uri': settings.REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
        }).prepare().url
        return JsonResponse({'url': url}, status=200)

"""This method gets a spotify generated access token if the user is authenticated
"""
def spotifyCallback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    #handle error
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if request.user.is_authenticated:
        update_or_create_user_tokens(request.user.username, access_token, token_type, expires_in, refresh_token)
    
    return redirect('partyupapp:playlist')

"""This method checks whether the user is authenticated by spotify
"""
def isSpotifyAuthenticated(request):
    if request.user.is_authenticated:
        is_authenticated = is_spotify_authenticated(request.user.username)
        return JsonResponse({'is_spotify_authenticated': is_authenticated}, status=200)        

"""This method loads the playlist page and its associated functionality
"""
def playlist(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')        
    if request.method == 'POST':
        if request.POST.get('song_list', None):
            playlist_name = request.POST.getlist('playlist_name')[0]
            track_list_str = request.POST.getlist('song_list')
            track_list = []
            for track in track_list_str:
                track_list.append(track.split('Name: ')[1])
            track_id_list_str = request.POST.getlist('song_id_list')
            track_id_list = track_id_list_str[0].split(',')
            if track_list == ['']:
                request.session['track_list'] = []
                request.session['playlist'] = playlist_name
                return JsonResponse({'message': 'Success'}, status=200)
            for i in range(len(track_list)):
                form = PartyPlaylistForm({'track_search': track_list[i], 'playlist_name': playlist_name, 'playlist_search': 'None', 'track_id': track_id_list[i]})
                if not form.is_valid():
                    return JsonResponse({'form_errors': 'Error searching playlist or tracks. Please try again later.'}, status=500)
            request.session['track_list'] = track_list
            request.session['track_id_list'] = track_id_list
            request.session['playlist'] = playlist_name
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            playlist_id = request.POST.get('playlist_id')
            form = PartyPlaylistForm({'track_search': 'None', 'playlist_name': 'None', 'playlist_search': playlist_id, 'track_id': 'None'})
            if form.is_valid():
                # Process data
                request.session['playlist_id'] = form.cleaned_data['playlist_search']
                return JsonResponse({'message': 'Success'}, status=200)
            return JsonResponse({'form_errors': form.errors.as_json(escape_html=True)}, status=500)
    else:
        form = PartyPlaylistForm()
        return render(request,'PartyUpApp/playlist.html', {'form': form})

"""This method executes spotify API requests initiated on the website
"""
def execute_spotify_api_request(username, endpoint, body=None, post_=False, put_=False, get_=False, delete_=False):
    tokens = get_user_tokens(username)
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens.access_token}

    if body:
        if post_:
            response = post(settings.SPOTIFY_BASE_URL + endpoint, json=body, headers=headers)
        elif put_:
            response = put(settings.SPOTIFY_BASE_URL + endpoint, json=body, headers=headers)
        elif get_:
            response = get(settings.SPOTIFY_BASE_URL + endpoint, json=body, headers=headers)
        elif delete_:
            response = delete(settings.SPOTIFY_BASE_URL + endpoint, json=body, headers=headers)
    else:
        if post_:
            response = post(settings.SPOTIFY_BASE_URL + endpoint, headers=headers)
        elif put_:
            response = put(settings.SPOTIFY_BASE_URL + endpoint, headers=headers)
        elif get_:
            response = get(settings.SPOTIFY_BASE_URL + endpoint, headers=headers)
        elif delete_:
            response = delete(settings.SPOTIFY_BASE_URL + endpoint, headers=headers)
    
    try:
        return response
    except:
        return {'Error': 'Error Issuing Request'}

"""This method implements the search track functionality
"""
def searchTracks(request):
    if not request.user.is_authenticated:
        return redirect('partupapp:login')
    term = request.GET.get('term')
    endpoint = f'search?q={term}&type=track&limit=5'
    response = execute_spotify_api_request(request.user.username, endpoint, get_=True)
    response = json.loads(response.content.decode('utf-8'))

    if 'error' in response or not 'items' in response.get('tracks'):
        return JsonResponse({'error': response.get('error')}, status=200)
    
    tracks = response.get('tracks')
    items = tracks.get('items')
    tracks_res = []

    for item in items:
        tracks_res.append(f"Name: {item.get('name')}, Id: {item.get('id')}")
    return JsonResponse(tracks_res, safe=False)

"""This method returns the current spotify user
"""
def getCurrentUser(request):
    if not request.user.is_authenticated:
        return redirect('partupapp:login')
    endpoint = 'me'
    response = execute_spotify_api_request(request.user.username, endpoint, get_=True)
    response = json.loads(response.content.decode('utf-8'))

    if 'error' in response:
        return JsonResponse({'error': response.get('error')}, status=500)
    
    spotify_id_json = json.loads(response.content.decode('utf-8'))
    spotify_id = spotify_id_json.get('id')

    return JsonResponse({'id': spotify_id}, status=200)  


"""This method returns the authorised user's playlist on spotify
"""
def getUserPlaylist(request):
    if not request.user.is_authenticated:
        return redirect('partupapp:login')
    id_json_res = getCurrentUser(request)
    id = json.loads(id_json_res.content.decode('utf-8'))
    if not id['id']:
        print('not id')
        return JsonResponse({'error': 'Error retrieving your playlists.'}, status=500)
    endpoint = f"users/{id['id']}/playlists?limit=10"
    response = execute_spotify_api_request(request.user.username, endpoint, get_=True)
    response = json.loads(response.content.decode('utf-8'))

    if 'error' in response or not 'items' in response:
        print('error or no items')
        return JsonResponse({'error': response.get('error')}, status=500)

    playlists = response.get('items')
    playlists_res = []
    for playlist in playlists:
        playlists_res.append(f"Name: {playlist.get('id')}, Id: {playlist.get('name')}")
    
    return JsonResponse(playlists_res, safe=False, status=200)  

"""Creates playlist for an event
"""
def createPlaylist(request, name):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    id_json_res = getCurrentUser(request)
    id = json.loads(id_json_res.content.decode('utf-8'))
    endpoint = f"users/{id['id']}/playlists"
    body = {
        'name': name,
        'public': 'false',
    }
    response = execute_spotify_api_request(request.user.username, endpoint, body=body, post_=True)
    response = json.loads(response.content.decode('utf-8'))

    if 'error' in response or not 'id' in response:
        return JsonResponse({'error': response.get('error')}, status=200)

    id = response.get('id')
    return JsonResponse(id, safe=False, status=200)  

"""Adds tracks to playlist
"""
def addTracksToPlaylist(request, id, uris):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    endpoint = f"playlists/{id}/tracks"
    body = {
        'uris': uris
    }
    response = execute_spotify_api_request(request.user.username, endpoint, body, post_=True)
    response = json.loads(response.content.decode('utf-8'))

    if 'error' in response or not 'snapshot_id' in response:
        return JsonResponse({'error': response.get('error')}, status=200)

    return JsonResponse(response.get('snapshot_id'), safe=False, status=200)  

"""Checks whether a request is AJAX or not
"""
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

"""Returns a list of all vendors registered on the website
"""
def vendor_list(request):
    if request.method == 'GET':
        vendors = list(Vendor.objects.all().filter())
        # if (is_ajax(request=request)):
        #     print (all)
            # return JsonResponse(vendors,safe=False)
        return render(request, 'PartyUpApp/vendor_list.html',{'vendors':vendors})
            
    return render(request, 'PartyUpApp/vendor_list.html')


"""Returns user profile details
"""
def user_profile(request):
    if request.user.is_authenticated: 
        form = UserUpdateForm(data=request.POST or None,instance=request.user) 
        if (request.method=="POST"):
            # form = UserUpdateForm(request.POST,instance=request.user)
            if form.is_valid():
                request.user.display_name = form.cleaned_data['display_name']
                request.user.email = form.cleaned_data['email']
                request.user.phone_number = form.cleaned_data['phone_number']
                # request.user.set_password(form.cleaned_data['password'])
                user = request.user.save()
                # update_session_auth_hash(request, request.user) 
                # form.save()
                messages.success(request,('Your profile was successfully updated!'))
            else:
                messages.error(request,('An error has occured'))
                # return render(request,'PartyUpApp/user_profile.html',{"form":form})
            return redirect('/partyup/user_profile/')
           
        return render(request,'PartyUpApp/user_profile.html',{"form":form})

    else:
        return redirect('/partyup/login/') 

"""Changes the user password using the change password form
"""
def change_password(request):
    if request.user.is_authenticated: 
        form = PasswordChangeForm(data=request.POST or None,user=request.user) 
        if (request.method=="POST"):
            if form.is_valid():
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request,('Your profile was successfully updated!')) 
            else:
                messages.error(request,('An error has occured'))
            return redirect('/partyup/change_password/')
        return render(request,'PartyUpApp/change_password.html',{"form":form})
    else:
        return redirect('/partyup/login/') 

"""Helper function for calculating the average rating"""
def calculate_avg_rating(ratings):
    avg_rating = 0
    total_ratings = 0
    for rating in ratings:
        avg_rating += rating.rating
        total_ratings += 1

    if total_ratings != 0:
        avg_rating = avg_rating / total_ratings

    return avg_rating

"""Retrieves and returns the details of a specific vendor
"""
def vendor_profile (request, vendor_id=None):
    if request.user.is_authenticated and request.user.is_vendor and (vendor_id is None or vendor_id == request.user.id):
        vendor=Vendor.objects.filter(user=request.user).first()
        vendor_form = VendorUpdateForm(data=request.POST or None,instance=vendor)
        user_form = UserUpdateForm(data=request.POST or None,instance=request.user)
        if (request.method=="POST"):
            # form = UserUpdateForm(request.POST,instance=request.user)
            if vendor_form.is_valid() and user_form.is_valid():
                request.user.display_name = user_form.cleaned_data['display_name']
                request.user.email = user_form.cleaned_data['email']
                request.user.phone_number = user_form.cleaned_data['phone_number']

                vendor.description = vendor_form.cleaned_data['description']
                vendor.price = vendor_form.cleaned_data['price']
                if (vendor.type=="Venue"):
                    vendor.address = vendor_form.cleaned_data['address']
                vendor.save()
                # form.save()
                messages.success(request,('Your profile was successfully updated!'))
            else:
                messages.error(request,('Please provide valid values for all fields'))
                # return render(request,'PartyUpApp/user_profile.html',{"form":form})
            return redirect('/partyup/vendor_profile/')
           
        return render(request,'PartyUpApp/vendor_profile.html',{"user_form":user_form,"vendor_form":vendor_form})

    elif request.user.is_authenticated and vendor_id is not None:
        if (request.method == "GET"):
            vendor_details = Vendor.objects.filter(user__id=vendor_id)
            ratings = Ratings.objects.filter(vendor_user=vendor_id)

            avg_rating = calculate_avg_rating(ratings)

            return render(request, 'PartyUpApp/vendor_profile_public.html', {"vendor_details": vendor_details[0], "rating" : avg_rating})
        if (request.method == "POST"):
            rating_form = VendorRatingForm(data=request.POST)

            if rating_form.is_valid():

                rating = rating_form.save(commit=False)

                rating.rating_user = request.user

                ratings_exist = Ratings.objects.filter(rating_user=request.user,vendor_user=vendor_id)
                if ratings_exist.exists() :
                    ratings_exist.update(rating=rating.rating)
                else:
                    rating.save()

            ratings = Ratings.objects.filter(vendor_user=vendor_id)

            avg_rating = calculate_avg_rating(ratings)

            return JsonResponse({'rating': avg_rating}, status=200)

    return redirect('/partyup')

"""Initiates the payment functionality and redirects to the payment page
"""
def payment(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    end = datetime.strptime(request.session.get('end_date'), '%Y-%m-%d %H:%M:%S%z')
    start = datetime.strptime(request.session.get('start_date'), '%Y-%m-%d %H:%M:%S%z')
    difference = end - start
    diff_in_sec = difference.total_seconds()
    hours = diff_in_sec / 60 / 60
    venue = request.session.get('venue_username')
    venue_price = 0
    if venue is not None:
        qs = Vendor.objects.filter(user__username=venue)
        if qs.exists():
            venue_price = qs[0].price

    vendor_prices = []
    vendor_list = request.session.get('vendor_list')
    for vendor in vendor_list:
        qs = Vendor.objects.filter(user__username=vendor)
        if qs.exists():
            vendor_prices.append(qs[0].price)
    total_price = venue_price
    for p in vendor_prices:
        to_add = hours * p
        total_price = total_price + to_add
    if request.method == 'GET':
        payment = round(total_price, 2)
        return render(request,'PartyUpApp/payment.html', {'payment' : payment})
    else:
        return render(request,'PartyUpApp/payment.html')

"""Enables the autocomplete functionality for venue when creating events
"""
def venue_autocomplete(request):
    if 'term' in request.GET:
        qs = Vendor.objects.filter(user__username__istartswith=request.GET.get('term'), type='Venue')
        vendors = list()
        for vendor in qs:
            vendors.append(vendor.user.username)
        return JsonResponse(vendors, safe=False)
    return render(request, 'PartyUpApp/choose_venue.html')

"""Enables the autocomplete functionality for vendors when creating a new event
"""
def vendor_autocomplete(request):
    if 'term' in request.GET:
        qs = Vendor.objects.filter(user__username__istartswith=request.GET.get('term')).exclude(type="Venue")
        vendors = list()
        for vendor in qs:
            vendors.append(vendor.user.username)
        return JsonResponse(vendors, safe=False)
    return render(request, 'PartyUpApp/hire_vendors.html')

"""Enables autocomplete functionality for guests when creating a new event
"""
def guest_autocomplete(request):
    if 'term' in request.GET:
        qs = User.objects.filter(username__istartswith=request.GET.get('term')).exclude(is_vendor=True).exclude(username=request.user)
        users = list()
        for user in qs:
            users.append(user.username)
        return JsonResponse(users, safe=False)
    return render(request, 'PartyUpApp/hire_vendors.html')

"""Retrives user info
"""
def guest_info(request):
    if 'username' in request.GET:
        qs = User.objects.filter(username=request.GET.get('username'))
        if qs.exists():
            user = {"username": qs[0].username, "first_name": qs[0].first_name, 
                "last_name": qs[0].last_name}
            return JsonResponse(user, safe=True)
        else:
            return JsonResponse({"error": "Vendor with username does not exist"}, safe=True)
    return render(request, 'PartyUpApp/hire_vendors.html')

"""Retrieves vendor info
"""
def vendor_info(request):
    if 'username' in request.GET:
        qs = Vendor.objects.filter(user__username=request.GET.get('username'))
        if qs.exists():
            vendor = {"username": qs[0].user.username, "first_name": qs[0].user.first_name, 
                "last_name": qs[0].user.last_name}
            return JsonResponse(vendor, safe=True)
        else:
            return JsonResponse({"error": "Vendor with username does not exist"}, safe=True)
    return render(request, 'PartyUpApp/hire_vendors.html')

"""Shows all the existing bookings for the current logged in vendor
"""
def view_bookings (request):
    # check if the user is authenticated
    if request.user.is_authenticated and request.user.is_vendor:
        if request.method=="GET":
            # get all the bookings
            bookings = list(Booking.objects.filter(vendor=request.user.id).values())
            return render(request,'PartyUpApp/view_bookings.html',{"bookings": bookings})
        return render(request,'PartyUpApp/view_bookings.html',{"bookings":[]}) 
    # If not logged in, redirect to the login page
    else:
        return redirect('/partyup/login/') 

""" Delete event with id
"""
def delete_event(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    if request.method == "POST":
        event = Event.objects.get(pk=request.POST.get('event_id'))
        if event:
            event.delete()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'error': 'Error deleting event, contact us or try again later.'}, status=500)
    return JsonResponse({'error': 'Error deleting event, contact us or try again later.'}, status=500)


""" Inserts event and all related objects (bookings, items, guests, transactions) 
    into database. This operation is atomic.
"""
@transaction.atomic
def finalise(request):
    if not request.user.is_authenticated:
        return redirect('partyupapp:login')
    # clear session variables and save objects
    if request.method == "POST":
        if not (request.session.get('track_list', None) or request.session.get('playlist_id', None)):
            if request.session.get('address', None):
                # create address object
                addr = Address(raw=request.session.get('address'))
                # write address to db
                addr.save()
                # create event
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id='None', address_id=addr.id, user_id=request.user.id)
                # clear session variables
                del request.session['address']
                del request.session['name']
                del request.session['description']
            else:
                venue_username = request.session.get('venue_username')
                venue = Vendor.objects.filter(user__username=venue_username)[0]
                addr = venue.address
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id='None', address_id=addr, user_id=request.user.id)
                # clear session variables
                del request.session['venue_username']
                del request.session['name']
                del request.session['description']
            # write event to db
            event.save()
        elif request.session.get('track_list', None):
            playlist_name = request.session.get('playlist')
            playlist_res = createPlaylist(request, playlist_name)
            if json.loads(playlist_res.content.decode('utf-8')) == 'error':
                del request.session['playlist']
                return JsonResponse({'error': 'Error Creating Playlist'})
            playlist_id = json.loads(playlist_res.content.decode('utf-8'))
            track_uri_list = []
            for track_id in request.session.get('track_id_list', None):
                track_uri = f"spotify:track:{track_id}"
                track_uri_list.append(track_uri)
            tracks_res = addTracksToPlaylist(request, playlist_id, track_uri_list)
            if json.loads(tracks_res.content.decode('utf-8')) == 'error':
                del request.session['track_id_list']
                return JsonResponse({'error': 'Error adding tracks to playlist'})
            # clear session variables
            del request.session['track_list']
            del request.session['playlist']
            del request.session['track_id_list']
            if request.session.get('address', None):
                addr = Address(raw=request.session.get('address'))
                addr = addr.save()
                # create event
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id=playlist_id, address_id=addr.id, user_id=request.user.id)
                # clear session variables
                del request.session['address']
                del request.session['name']
                del request.session['description']
            else:
                venue_username = request.session.get('venue_username')
                venue = Vendor.objects.filter(user__username=venue_username)[0]
                addr = venue.address
                # create event
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id=playlist_id, address_id=addr, user_id=request.user.id)
                # clear session variables
                del request.session['venue_username']
                del request.session['name']
                del request.session['description']
            # write event to db
            event.save()
        else:
            if request.session.get('address', None):
                addr = Address(raw=request.session.get('address'))
                addr.save()
                # create event
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id=request.session.get('playlist_id'), address_id=addr.id, user_id=request.user.id)
                del request.session['address']
                del request.session['name']
                del request.session['description']
            else:
                venue_username = request.session.get('venue_username')
                venue = Vendor.objects.filter(user__username=venue_username)[0]
                addr = venue.address
                # create event
                event = Event(name=request.session.get('name'), description=request.session.get('description'), playlist_id=request.session.get('playlist_id'), address_id=addr, user_id=request.user.id)
                del request.session['venue_username']
                del request.session['name']
                del request.session['description']
            # write event to db
            event.save()    
        for guest in request.session.get('guest_list', None):
            guest_id = User.objects.filter(username=guest)[0].id
            # create guest
            guest = Guest(event_id=event.id, user_id=guest_id)
            # write guest to db
            guest.save()
        for item in request.session.get('item_list', None):
            # create item
            item = Item(name=item, description=None, acquired=False, event_id=event.id)
            # write item to db
            item.save()
        for vendor in request.session.get('vendor_list', None):
            vendor_id = Vendor.objects.filter(user__username=vendor)[0].user.id
            # create booking
            booking = Booking(start_date=request.session.get('start_date'), end_date=request.session.get('end_date'), event_id=event.id, user_id=request.user.id, vendor_id=vendor_id, vendor_name=vendor)
            # write booking to db
            booking.save()
        if request.POST.get('payment'):
            # create transaction
            transaction = Transaction(amount=request.POST.get('payment'), event_id=event.id, user_id=request.user.id)
            # write transaction to db
            transaction.save()
        del request.session['guest_list']
        del request.session['item_list']
        del request.session['vendor_list']
        del request.session['start_date']
        del request.session['end_date']
        return JsonResponse({'message': 'Success'}, status=200)
    return JsonResponse({'error': 'Error Processing Payment'}, status=500)
    
