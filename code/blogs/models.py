from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from properties.models import PropertySubCategory
import os


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    sub_category = models.ForeignKey(PropertySubCategory, on_delete=models.CASCADE, default=1)
    content = models.TextField()  # Replaced RichTextField with TextField
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.image:
            ext = os.path.splitext(self.image.name)[1]
            self.image.name = os.path.join('', f"{self.slug}{ext}")
        
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
