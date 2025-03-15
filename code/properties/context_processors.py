from django.db.models import Count, Q
from .models import PropertyCategory
def property_categories(request):
    categories = PropertyCategory.objects.prefetch_related(
        'subcategories'
    ).filter(
        subcategories__property__isnull=False
    ).order_by('name').distinct()

    for category in categories:
        category.filtered_subcategories = category.subcategories.annotate(
            total_properties=Count('property')
        ).filter(total_properties__gt=0)

    return {'property_categories': categories}
