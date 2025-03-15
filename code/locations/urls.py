from django.urls import path
from .views import StateAutocomplete, CityAutocomplete, AreaAutocomplete

urlpatterns = [
    path('state-autocomplete/', StateAutocomplete.as_view(), name='state-autocomplete'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('area-autocomplete/', AreaAutocomplete.as_view(), name='area-autocomplete'),
]
