from django.db import models
import os
import io
from django.core.files.base import ContentFile
from PIL import Image
from django.utils.text import slugify

# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # Slug field added
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    pincode = models.CharField(max_length=6, null=True, blank=True) 
    image = models.ImageField(upload_to="city/", null=True, blank=True) 

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)

        # Process image and save as JPG
        if self.image:
            filename = f"{self.slug}.jpg"  #
            file_path = os.path.join("", filename)

            image = Image.open(self.image)
            image = image.convert("RGB")  

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=80)
            buffer.seek(0)

            self.image.save(file_path, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")
    # pincode field is removed

    def __str__(self):
        return f"{self.name}, {self.city.name}"
