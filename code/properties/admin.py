from django.contrib import admin
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from .models import User, PropertyCategory, PropertySubCategory, Property, PropertyImage, Inquiry, Favorite,AmenityCategory, Amenity,FloorPlan,Nearby,Tag,Project,Builder,ProjectPriceList,ProjectSpecification
from django import forms
from locations.models import State,City,Area

class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') 
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
class PropertySubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image','homefeed', 'get_category')  # Fix: Use correct property name
    search_fields = ('name', 'slug','homefeed')
    prepopulated_fields = {'slug': ('name',)}
    def get_category(self, obj):
        return obj.category.name  # Since subcategory has a single category now
    
    get_category.short_description = "Category"  # Sets column title in Django Admin

class CategoryFilter(SimpleListFilter):
    title = _('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = PropertyCategory.objects.all()
        return [(cat.id, cat.name) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sub_category__category__id=self.value())
        return queryset
    
class AmenityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'category')  # Display category in the list
    list_filter = ('category',)  # Add filter for categories
    search_fields = ('name', 'category__name') 
    
 
class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1  # Allows adding multiple files
    
class ProjectPriceListInline(admin.TabularInline):
    model = ProjectPriceList
    extra = 1  # Allows adding multiple files
    
class ProjectSpecificationInline(admin.TabularInline):
    model = ProjectSpecification
    extra = 1  # Allows adding multiple files

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    
class NearbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')  
    prepopulated_fields = {'slug': ('name',)}
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')  
    
class BuilderAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')  
    prepopulated_fields = {'slug': ('name',)}
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'builder')  
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProjectPriceListInline,ProjectSpecificationInline]

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete'),
            'sub_category': autocomplete.ModelSelect2(
                url='sub-category-autocomplete',
                forward=['category']
            ),
            'state': autocomplete.ModelSelect2(url='state-autocomplete'),
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete',
                forward=['state']
            ),
            'area': autocomplete.ModelSelect2(
                url='area-autocomplete',
                forward=['city']
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_project_based'].widget = forms.HiddenInput()
        
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "sub_category":
        kwargs["queryset"] = PropertySubCategory.objects.all()
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PropertyAdmin(admin.ModelAdmin):
    form = PropertyForm
    list_display = ('title', 'get_category', 'sub_category', 'price', 'location', 'status')
    search_fields = ('title', 'sub_category__name', 'location')
    list_filter = ('status', CategoryFilter)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FloorPlanInline,PropertyImageInline]
    
    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',  # Include jQuery
            'js/property_admin.js',  # Custom JS
        )
    def get_category(self, obj):
        return obj.sub_category.category.name if obj.sub_category and obj.sub_category.category else "N/A"
    
    get_category.short_description = "Category"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            assigned_projects = list(Property.objects.values_list('project', flat=True).distinct())
            
            # Get the object being edited
            obj_id = request.resolver_match.kwargs.get('object_id')  # Get the ID of the object being edited
            if obj_id:
                current_project = Property.objects.filter(id=obj_id).values_list('project', flat=True).first()
                if current_project:
                    assigned_projects.remove(current_project)  # Allow the current project's selection
                
            kwargs["queryset"] = Project.objects.exclude(id__in=assigned_projects) if assigned_projects else Project.objects.all()

        if db_field.name == "sub_category":
            kwargs["queryset"] = PropertySubCategory.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"


class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property', 'image')
    list_filter = ('property', 'image')
    
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phone','created_at')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')

    
admin.site.register(User)
admin.site.register(PropertyCategory, PropertyCategoryAdmin)
admin.site.register(PropertySubCategory, PropertySubCategoryAdmin)
admin.site.register(AmenityCategory,AmenityCategoryAdmin)
admin.site.register(Amenity,AmenityAdmin)
admin.site.register(Builder,BuilderAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Nearby,NearbyAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(FloorPlan)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(Inquiry,InquiryAdmin)
admin.site.register(Favorite)

