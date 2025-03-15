from django.contrib import admin
from .models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'icon', 'category', 'slug')  

admin.site.register(Service, ServiceAdmin)
