from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Service

class ServicesView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    queryset = Service.objects.all()

class ServicesDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'post'