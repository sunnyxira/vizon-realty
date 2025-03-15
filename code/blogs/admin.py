from django.contrib import admin
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
        widgets = {
            'content': forms.Textarea(attrs={'class': 'trix-content'})
        }

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm

    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/trix/2.0.0/trix.min.js",
            "js/trix_admin.js",
        ]
        css = {
            "all": ["https://cdnjs.cloudflare.com/ajax/libs/trix/2.0.0/trix.min.css"]
        }

admin.site.register(BlogPost, BlogPostAdmin)
