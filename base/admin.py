from django.contrib import admin
from .models import User, Profile, GeneratedImage, EnhancedImage, ColorizedImage

# Register your models here.
admin.site.register(Profile)
admin.site.register(GeneratedImage)
admin.site.register(EnhancedImage)
admin.site.register(ColorizedImage)
