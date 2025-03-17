# Handle URLs from 'pixelplexus' folder
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path('register/', views.registerUser, name= 'register'),

    path('login/', views.loginUser, name= 'login'),
    path('logout/', views.logoutUser, name= 'logout'),

    path('', views.home, name= 'home'),

    path('profile/<int:pk>/', views.userProfile, name= 'profile'),
    path('update_profile/<int:pk>/', views.updateProfile, name= 'update-profile'),

    path('image_generation/', views.imageGeneration, name= 'image-generation'),
    path('delete-generated-image/<int:image_id>/', views.delete_generated_image, name='delete-generated-image'),

    path('image_enchancement/', views.imageEnhancement, name= 'image-enhancement'),
    path('delete-enhanced-image/<int:image_id>/', views.delete_enhanced_image, name='delete-enhanced-image'),

    path('image_colorization/', views.imageColorization, name= 'image-colorization'),
    path('delete-colorized-image/<int:image_id>/', views.delete_colorized_image, name='delete-colorized-image'),

    path('output-image/<int:image_id>/', views.outputImage, name='output-image'),
]

urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)