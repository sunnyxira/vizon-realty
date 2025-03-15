from dal import autocomplete
from django.shortcuts import render
from .models import City, Area,State

class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return State.objects.none()
        return State.objects.all()


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        queryset = City.objects.all()
        state_id = self.forwarded.get('state', None)

        if state_id:
            queryset = queryset.filter(state_id=state_id)

        return queryset

class AreaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Area.objects.none()

        queryset = Area.objects.all()
        city_id = self.forwarded.get('city', None)

        if city_id:
            queryset = queryset.filter(city_id=city_id)

        return queryset
