from django.shortcuts import render
from dal import autocomplete
from rest_framework import viewsets
from .models import PropertyCategory, PropertySubCategory, Property, PropertyImage, Inquiry, Favorite
from .serializers import PropertyCategorySerializer, PropertySubCategorySerializer, PropertySerializer, PropertyImageSerializer, InquirySerializer, FavoriteSerializer

class PropertyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertyCategory.objects.all()
    serializer_class = PropertyCategorySerializer

class PropertySubCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertySubCategory.objects.all()
    serializer_class = PropertySubCategorySerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PropertyCategory.objects.none()

        qs = PropertyCategory.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
    
class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PropertySubCategory.objects.none()

        qs = PropertySubCategory.objects.all()

        # Filter by selected category (forwarded from PropertyForm)
        category_id = self.forwarded.get('category', None)
        if category_id:
            qs = qs.filter(category_id=category_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
