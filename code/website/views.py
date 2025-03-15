from django.shortcuts import render, get_object_or_404, redirect
from properties.models import PropertyCategory, PropertySubCategory, Property,PropertyImage,AmenityCategory,FloorPlan,Inquiry,Builder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.contrib import messages
from blogs.models import BlogPost
from services.models import Service
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate,logout
from users.models import User
from locations.models import City, State,Area
from django.views.decorators.csrf import csrf_exempt


def home(request):
    
    property_categories = PropertyCategory.objects.order_by('name').filter(subcategories__isnull=False).distinct().prefetch_related("subcategories").order_by('name')
    property_subcategories = PropertySubCategory.objects.all()
    homefeedview = PropertySubCategory.objects.filter(image__isnull=False, homefeed=True)
    propertyList = Property.objects.all()
    posts = BlogPost.objects.all()
    services = Service.objects.all()
    cities = City.objects.annotate(property_count=Count("properties"))
    featuredbuilderproperties = Property.objects.filter(project__featured_project=True)
    builders = Builder.objects.all()
    context = {
        'categories': property_categories,
        'sub_categories': property_subcategories,
        'homefeed': homefeedview,
        'properties': propertyList,
        'fb_properties': featuredbuilderproperties,
        'posts': posts,
        'builders': builders,
        'services': services,
        'cities': cities,
        'page_title': 'Vizon Realty'
    }
    
    return render(request, 'index/index.html',context)

def load_subcategories(request):
    category_id = request.GET.get('category_id')  
    subcategories = PropertySubCategory.objects.filter(category=category_id) 
    gert = request.session.get("subcategories", [])
    return render(request, "property/load_sub_categories.html", {"subcategories": subcategories,"gert":gert})

def property_search(request):
    if request.method == "POST":
        request.session["category"] = request.POST.get("category")
        request.session["subcategories"] = request.POST.getlist("subcategories")
        request.session["transaction_type"] = request.POST.get("transaction")
        request.session["location"] = request.POST.get("location")

    category = request.session.get("category")
    subcategories = request.session.get("subcategories", [])
    transaction_type = request.session.get("transaction_type")
    location = request.session.get("location")

    properties = Property.objects.all()

    if category:
        properties = properties.filter(sub_category__category_id=category)

    if subcategories:
        subcategories = list(map(int, subcategories))  
        properties = properties.filter(sub_category__id__in=subcategories)

    if transaction_type:
        properties = properties.filter(transaction_type=transaction_type)

    if location:
        properties = properties.filter(location__icontains=location)

    
    property_categories = PropertyCategory.objects.order_by('name').filter(subcategories__isnull=False).distinct().prefetch_related("subcategories").order_by('name')
    property_subcategories = PropertySubCategory.objects.all()
    
    context = {
        'properties': properties,
        'session_data': request.session,  
        'categories': property_categories,
        'sub_categories': property_subcategories,
    }
    return render(request, 'property/list_search.html', context)


def property_list(request, slug=None, filter_type=None):
    properties = Property.objects.all()
    page_title = "Properties"
    
    if slug and filter_type == "subcategory":
        obj = get_object_or_404(PropertySubCategory, slug=slug)
        properties = properties.filter(sub_category=obj)
        page_title = obj.name

    elif slug and filter_type == "city":
        obj = get_object_or_404(City, slug=slug)
        properties = properties.filter(city__slug=slug)
        page_title = f"Properties in {obj.name}"

    property_categories = PropertyCategory.objects.filter(subcategories__isnull=False)\
        .distinct().prefetch_related("subcategories").order_by("name")

    context = {
        'properties': properties,
        'filter_obj': obj if slug else None,
        'categories': property_categories,
        'page_title': page_title
    }
    
    return render(request, 'property/list_search.html', context)


def property_detail(request,uniqueid, slug):
    property_obj = get_object_or_404(Property, listing_id=uniqueid, slug=slug)
    floor_plans = FloorPlan.objects.filter(property=property_obj)
    nearby = property_obj.nearby.all()

    amenities_by_category = {}
    for category in AmenityCategory.objects.prefetch_related("amenities"):
        amenities = category.amenities.filter(properties=property_obj)  
        if amenities.exists():
            amenities_by_category[category] = amenities

    context = {
        'property': property_obj,
        'amenities_by_category': amenities_by_category,
        'floor_plans': floor_plans,
        'nearby': nearby,
        'page_title': property_obj.title,
    }

    return render(request, 'property/details.html', context)

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')

def add_new_property(request):
    return render(request, 'add_new_property.html')

def property_inquiry(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            messages.error(request, 'Invalid property selected.')
            return redirect('thank_you')

        inquiry = Inquiry(
            property=property_obj,
            message=message,
            name=name,
            email=email,
            phone=phone,
            status='pending'
        )

        if request.user.is_authenticated:
            inquiry.user = request.user
        else:
            inquiry.user = None  # Default to null if not logged in

        inquiry.save()

        messages.success(request, 'Your inquiry has been submitted successfully!')
        return redirect('thank_you')

    messages.error(request, 'Failed to submit inquiry. Please try again.')
    return redirect('thank_you')

def complete_registration(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        name = request.POST.get("name")
        email = request.POST.get("email")
        is_agent = request.POST.get("is_agent")

        if not phone or not name or not email:
            return JsonResponse({"success": False, "error": "All fields are required"}, status=400)

        # Check if user exists
        user, created = User.objects.get_or_create(phone=phone, defaults={"name": name, "email": email})

        if not created:
            # Update the existing user
            user.name = name
            user.email = email
            user.role = "Agent" if is_agent == "yes" else "User"
            user.save()

        # Ensure user has a password for authentication
        if not user.password:
            user.set_password("default_password")  # Set a default password if none exists
            user.save()

        # Authenticate using custom phone backend
        user = authenticate(request, phone=phone, password="default_password")
        if user:
            login(request, user)
            return JsonResponse({"success": True, "message": "User registered & logged in"})
        else:
            return JsonResponse({"success": False, "error": "Authentication failed"}, status=400)

def user_login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")  # This should be pin in your model

        if not phone or not password:
            return JsonResponse({"success": False, "error": "Both phone and pin are required"}, status=400)

        user = authenticate(request, phone=phone, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful"}) 

        # If user does not exist, prompt for additional details
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_password(password)  # Storing password as pin
            user.save()
            return JsonResponse({"success": True, "new_user": True, "message": "New user detected. Please complete registration."})

        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

def user_logout(request):
    logout(request)
    return redirect('/')
