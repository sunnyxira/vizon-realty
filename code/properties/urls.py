from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyCategoryViewSet, PropertySubCategoryViewSet, PropertyViewSet, PropertyImageViewSet, InquiryViewSet, FavoriteViewSet,CategoryAutocomplete, SubCategoryAutocomplete

router = DefaultRouter()
router.register(r'categories', PropertyCategoryViewSet)
router.register(r'sub-categories', PropertySubCategoryViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'images', PropertyImageViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('sub-category-autocomplete/', SubCategoryAutocomplete.as_view(), name='sub-category-autocomplete'),
]
