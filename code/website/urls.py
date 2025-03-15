from django.urls import path
from . import views
from .views import load_subcategories,property_list,property_search,property_detail,property_inquiry,complete_registration, user_login,user_logout
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path("load-subcategories/", load_subcategories, name="load_subcategories"),

    path('property/inquiry/', property_inquiry, name='property_inquiry'),
    
    path('properties/', property_list, name='all_properties'),
    path('properties/category/<slug:slug>/', property_list, {'filter_type': 'subcategory'}, name='property_by_category'),
    path('properties/city/<slug:slug>/', property_list, {'filter_type': 'city'}, name='property_by_city'),
    
    path('properties/<str:uniqueid>/<slug:slug>/', property_detail, name='property_detail'),

    path('search/property', property_search, name='property_search'),
    path('thank-you/', TemplateView.as_view(template_name="thank_you.html"), name='thank_you'),

    path('about_us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact, name='contact'), 
    path('add-new-property/', views.add_new_property, name='add_new_property'), 
    
    path('complete_registration/', complete_registration, name='complete_registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
