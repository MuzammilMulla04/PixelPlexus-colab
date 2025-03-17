from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
import os
import uuid

def user_avatar_upload_path(instance, filename):
    base_name, extension = os.path.splitext(filename)
    new_filename = f"profile-{instance.user.id}{extension}"
    return os.path.join('avatars/', new_filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_path, default='avatars/avatar.svg', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Function to generate unique file paths for generated images
def generated_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # Extracts file extension
    new_filename = f"profile_{instance.profile.id}_{uuid.uuid4().hex}{ext}"
    return os.path.join('generated_images/', new_filename)

class GeneratedImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generated_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generated Image by {self.profile.user.username}"
    @property
    def image_url(self):
        return self.image.url if self.image else ''

# Signal to delete image files when a GeneratedImage instance is deleted
@receiver(models.signals.post_delete, sender=GeneratedImage)
def delete_generated_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

# Function to generate unique file paths for enhanced images
def enhanced_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # Extracts file extension
    new_filename = f"profile_{instance.profile.id}_{uuid.uuid4().hex}{ext}"
    return os.path.join('enhanced_images/', new_filename)

class EnhancedImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=enhanced_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enhanced Image by {self.profile.user.username}"
    @property
    def image_url(self):
        return self.image.url if self.image else ''

# Signal to delete image files when a EnhancedImage instance is deleted
@receiver(models.signals.post_delete, sender=EnhancedImage)
def delete_enhanced_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

# Function to generate unique file paths for colorized images
def colorized_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # Extracts file extension
    new_filename = f"profile_{instance.profile.id}_{uuid.uuid4().hex}{ext}"
    return os.path.join('colorized_images/', new_filename)

class ColorizedImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=colorized_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Colorized Image by {self.profile.user.username}"
    @property
    def image_url(self):
        return self.image.url if self.image else ''

# Signal to delete image files when a ColorizedImage instance is deleted
@receiver(models.signals.post_delete, sender=ColorizedImage)
def delete_colorized_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
