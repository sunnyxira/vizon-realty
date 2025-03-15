from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import io
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from locations.models import State, City, Area
from users.models import User
from django.db import transaction, IntegrityError
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files import File
from datetime import datetime

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class PropertySubCategory(models.Model):
    category = models.ForeignKey(
        "PropertyCategory", 
        on_delete=models.CASCADE, 
        related_name="subcategories", 
        default=1
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="property_subcategory/", null=True, blank=True)
    homefeed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.image:
            filename = f"{self.slug}.webp"
            file_path = os.path.join("", filename)
            image = Image.open(self.image)
            image = image.convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP", quality=80)
            buffer.seek(0)
            self.image.save(file_path, ContentFile(buffer.read()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class AmenityCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(AmenityCategory, on_delete=models.CASCADE, related_name="amenities")

    def save(self, *args, **kwargs):
        if self.icon:
            ext = os.path.splitext(self.icon.name)[1]  # Get file extension
            self.icon.name = os.path.join('amenities_icons/', f"{slugify(self.name)}{ext}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Nearby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to="nearby_icon/", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.icon:
            filename = f"{self.slug}.webp"
            file_path = os.path.join("", filename)
            image = Image.open(self.icon)
            image = image.convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP", quality=80)
            buffer.seek(0)
            self.icon.save(file_path, ContentFile(buffer.read()), save=False)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, help_text="Hex color code (e.g., #FF5733)")

    def __str__(self):
        return self.name
    
class Builder(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to="builders/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.logo:
            filename = f"{self.slug}.webp"
            file_path = os.path.join("", filename)
            image = Image.open(self.logo)
            image = image.convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP", quality=80)
            buffer.seek(0)
            self.logo.save(file_path, ContentFile(buffer.read()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):

    name = models.CharField(max_length=255)  
    slug = models.SlugField(unique=True, blank=True)  
    builder = models.ForeignKey(Builder, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")  
    description = models.TextField(null=True, blank=True)  
    rough_price_range = models.CharField(max_length=255, help_text="Example: 50L - 1.5Cr")  
    total_units = models.IntegerField(null=True, blank=True)  
    project_size = models.CharField(max_length=255, help_text="Example: 7.74 Acres")  
    possession_start_date = models.DateField(null=True, blank=True)  
    avg_price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  
    rera_id = models.CharField(max_length=255, null=True, blank=True, help_text="RERA Registration ID")  
    configurations  = models.CharField(max_length=255, null=True, blank=True, help_text="2 & 3 bhk bungalows")  
    notes = models.TextField(null=True, blank=True)  
    featured_project = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
   
class ProjectPriceList(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="price_list")
    unit_type = models.CharField(max_length=50)  
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    super_built_up_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_final_price(self):
        total_price = self.base_price if self.base_price else 0
        return total_price

    def save(self, *args, **kwargs):
        self.final_price = self.calculate_final_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.unit_type} ({self.carpet_area} Sq. Ft.)"

class ProjectSpecification(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="specifications")
    title = models.CharField(max_length=255)  # e.g., "Power Backup", "Security"
    description = models.TextField(null=True, blank=True)  # Optional detailed description

    def __str__(self):
        return f"{self.project.name} - {self.title}"


def generate_unique_listing_id():
    return uuid.uuid4().hex[:10]

def generate_unique_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug)
    if qs.exists():
        slug = f"{slug}-{qs.count()}"
    return slug

class Property(models.Model):
    # Choices
    RATE_TYPE_CHOICES = [
        ('direct', 'Direct'),
        ('sqfeet', 'Sq. Feet')
    ]
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('rent', 'Rent'),
        ('lease', 'Lease'),
        ('invest', 'Invest') 
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented')
    ]

    # Basic Details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    listing_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name="properties")
    is_project_based = models.BooleanField(null=True,default=False)
    category = models.ForeignKey('PropertyCategory', on_delete=models.CASCADE, related_name="properties", null=True, blank=True)
    sub_category = models.ForeignKey('PropertySubCategory', on_delete=models.CASCADE)
    

    # Transaction Details
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, null=True, blank=True)
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES, default='direct')
    rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Size and Dimensions
    size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_area = models.CharField(max_length=255, null=True, blank=True)
    parking_area = models.CharField(max_length=255, null=True, blank=True)
    terrace_area = models.CharField(max_length=255, null=True, blank=True)
    dimension_size = models.CharField(max_length=50, null=True, blank=True, help_text="Example: 11x30")

    # Location Details (Fix applied here)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="properties", null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="properties", null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="properties", null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)


    # Property Features
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    amenities = models.ManyToManyField('Amenity', related_name="properties", blank=True)
    nearby = models.ManyToManyField('Nearby', related_name="properties", blank=True)

    # Media and Attachments
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    get_direction = models.TextField(null=True, blank=True)

    # Tags and Status
    tags = models.ManyToManyField('Tag', related_name="properties", blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        self.is_project_based = bool(self.project) 
        super().save(*args, **kwargs)
        
        # Ensure valid category-subcategory relationship
        if self.sub_category and self.category and self.sub_category.category != self.category:
            raise ValueError("Subcategory must belong to the selected category.")

        # Calculate price
        if self.rate_type == 'sqfeet' and self.rate and self.size:
            self.price = self.rate * self.size
        elif self.rate_type == 'direct' and self.rate:
            self.price = self.rate

        # Generate unique listing_id
        if not self.listing_id:
            unique = False
            while not unique:
                temp_id = uuid.uuid4().hex[:10]
                if not Property.objects.filter(listing_id=temp_id).exists():
                    self.listing_id = temp_id
                    unique = True

        # Generate unique slug
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

        # Atomic transaction to avoid duplication issues
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            self.listing_id = None  # Reset listing_id and retry
            self.save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.listing_id})"

    @property
    def get_category(self):
        """Get category from the related sub_category."""
        return self.sub_category.category if self.sub_category else None

def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "sub_category":
        kwargs["queryset"] = PropertySubCategory.objects.all()
    return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FloorPlan(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="property_floor_plans")
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="floor_plans/")

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1]  # Get file extension
            random_number = uuid.uuid4().hex[:4]
            self.file.name = f"{slugify(self.name)}-{random_number}{ext}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.property.title} - {self.name}"
    
    
class PropertyImage(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="property_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Save initially to generate file path
        if not self.pk:
            super().save(*args, **kwargs)

        img_path = self.image.path
        img = Image.open(img_path)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        jpg_filename = f"{timestamp}.jpg"
        jpg_path = os.path.join(os.path.dirname(img_path), jpg_filename)

        # Convert and save as JPG
        img.convert("RGB").save(jpg_path, "JPEG", quality=100, optimize=True)

        # Save the new JPG image
        with open(jpg_path, "rb") as f:
            self.image.save(f"{jpg_filename}", File(f), save=False)

        super().save(update_fields=["image"])

        # Remove original file if it's not already a JPG
        if os.path.exists(img_path) and img_path.lower() != jpg_path.lower():
            os.remove(img_path)

class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    name = models.CharField(max_length=255,default=None)
    email = models.CharField(max_length=255,default=None)
    phone = models.CharField(max_length=255,default=None)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

