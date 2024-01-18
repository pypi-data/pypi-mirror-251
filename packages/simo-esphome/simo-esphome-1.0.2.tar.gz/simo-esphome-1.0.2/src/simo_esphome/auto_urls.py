from django.urls import path
from django.conf.urls import url

from .autocomplete_views import BoardSelectAutocomplete, PinsSelectAutocomplete
from .views import firmware_status_view, rebuild_firmware_view, wifi_update_view


urlpatterns = [
    path(
        'autocomplete-espboard',
        BoardSelectAutocomplete.as_view(), name='autocomplete-espboard'
    ),
    path(
        'autocomplete-espboard-pins',
        PinsSelectAutocomplete.as_view(), name='autocomplete-espboard-pins'
    ),
    url(
        r'^firmware-status/(?P<id>[0-9]+)/$', firmware_status_view,
    ),
    url(
        r'^rebuild-firmware/(?P<id>[0-9]+)/$', rebuild_firmware_view,
    ),
    url(
        r'^wifi-update/(?P<id>[0-9]+)/$', wifi_update_view,
    )
]
