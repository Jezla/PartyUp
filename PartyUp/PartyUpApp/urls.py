from email import policy
from django.urls import path,re_path
from . import views

app_name = 'partyupapp'
urlpatterns = [
    path('', views.index, name='home'), # index (initial path)
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit/', views.submit, name='submit'),
    path('privacy/', views.policy, name='privacy'),
    path('faq/', views.faq, name='faq'),
    path('create_event/', views.create_event, name='create_event'),
    path('choose_venue/', views.choose_venue, name='choose_venue'),
    path('venue_autocomplete/', views.venue_autocomplete, name='venue_autocomplete'),
    path('vendor_autocomplete/', views.vendor_autocomplete, name='vendor_autocomplete'),
    path('guest_autocomplete/', views.guest_autocomplete, name='guest_autocomplete'),
    path('hire_vendors/', views.choose_vendors, name='choose_vendors'),
    path('invite_guests/', views.invite_guest, name='invite_guests'),
    path('checklist/', views.checklist, name='checklist'),
    path('vendor_info/', views.vendor_info, name='vendor_info'),
    path('guest_info/', views.guest_info, name='guest_info'),
    path('spotify/redirect', views.spotifyCallback, name='spotify_callback'),
    path('spotify/is_authenticated', views.isSpotifyAuthenticated, name='is_spotify_auth'),
    path('spotify/get_auth_url', views.spotifyAuthURL, name='spotify_auth'),
    path('spotify/searchTracks', views.searchTracks, name='search_tracks'),
    path('spotify/searchPlaylist', views.getUserPlaylist, name='search_playlist'),
    path('playlist/', views.playlist, name='playlist'),
    path('user_home/', views.user_home, name='user_home'),
    path('vendor_home/', views.vendor_home, name='vendor_home'),
    path('party_hub/', views.party_hub, name='party_hub'),
    path('logout/', views.logout_view, name='logout'),
    path('event_page/<int:event_id>/', views.event_page, name='event_page'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('payments/', views.payment, name='payment'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('vendor_profile/', views.vendor_profile, name='vendor_profile'),
    path('vendor_profile/<int:vendor_id>/', views.vendor_profile, name='vendor_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('payments/finalise', views.finalise, name='finalise_payment'),
    path('event/delete', views.delete_event, name='delete_event')
]