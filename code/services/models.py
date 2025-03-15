from django.db import models
from django.utils.text import slugify
from properties.models import PropertySubCategory  
import os
import os
import io
from PIL import Image
from django.core.files.base import ContentFile

class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(PropertySubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.ImageField(upload_to="services_icon/", null=True, blank=True)

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