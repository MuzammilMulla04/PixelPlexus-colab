from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, GeneratedImage, EnhancedImage, ColorizedImage
from .forms import RegistrationForm, ProfileForm
from ml_models.generation.inference import generate_image
from ml_models.enhancement.inference import enhance_image
from ml_models.colorization.inference import colorize_image

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('profile', pk= request.user.id)

    page = 'register'
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            Profile.objects.create(
                user= user,
                avatar= 'avatars/avatar.svg',
                bio= "Hi, I'm using PixelPlexus!"
            )

            login(request, user)
            return redirect('profile', pk= request.user.id)
        else:
            messages.error(request, 'An error occurred during Registration!')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        user= User.objects.get(id= request.user.id)
        user_profile = Profile.objects.get(user_id= user.id)
        return redirect('profile', pk= user_profile.user.id)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')
            return redirect('register')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'Incorrect credentials!')
            return redirect('register')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    context = {'id': request.user.id}  # This is still using the user id for rendering
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def userProfile(request, pk=None):
    user= User.objects.get(id= pk)
    user_profile= Profile.objects.get(user_id= user.id)

    # Fetch all images for the profile
    generated_images = GeneratedImage.objects.filter(profile= user_profile).order_by('-created_at')
    enhanced_images = EnhancedImage.objects.filter(profile= user_profile).order_by('-created_at')
    colorized_images = ColorizedImage.objects.filter(profile= user_profile).order_by('-created_at')

    context = {'user_profile': user_profile, 'generated_images': generated_images, 'enhanced_images': enhanced_images, 'colorized_images': colorized_images}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateProfile(request, pk):
    user= User.objects.get(id= pk)
    user_profile = Profile.objects.get(user_id= user.id)
    profile_form = ProfileForm(instance= user_profile)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance= user_profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', pk= pk)
        else:
            profile_form = ProfileForm(instance=user_profile)
            messages.error(request, 'An error occurred during profile update!')

    context = {'profile_form': profile_form}
    return render(request, 'base/update_profile.html', context)

def imageGeneration(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'User profile does not exist!')
            return redirect('login')

        prompt= request.POST.get("prompt", "")
        if not prompt:
            messages.error(request, 'Prompt cannot be empty!')
            return redirect('image-generation')

        # image = request.FILES['image']
        profile = Profile.objects.get(user= request.user)
        if not profile:
            messages.error(request, 'User profile does not exist!')
            redirect('login')

        image_path = generate_image(prompt)

        # Save generated image in DB
        generated_image = GeneratedImage.objects.create(profile=profile, image=image_path)
        messages.success(request, 'Image generated successfully!')
        latest_image = GeneratedImage.objects.filter(profile=profile).latest('created_at')

        return redirect('output-image', image_id=latest_image.id)
            
    return render(request, 'base/image_generation.html')
@login_required(login_url='login')
def delete_generated_image(request, image_id):
    """Handles image deletion by the authenticated user"""
    image = get_object_or_404(GeneratedImage, id=image_id)
    if not image:
        messages.error(request, 'Image does not exist!')

    # Ensure the user owns the image before deleting
    if request.user.profile == image.profile:
        image.delete()
        messages.success(request, 'Image was successfully deleted!')
    
    return redirect('profile', pk= request.user.id)

def imageEnhancement(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'User profile does not exist!')
            return redirect('login')

        if 'image' not in request.FILES:
            messages.error(request, 'No image file provided!')
            return redirect('image-enhancement')

        image = request.FILES['image']
        profile = Profile.objects.get(user=request.user)
        if not profile:
            messages.error(request, 'User profile does not exist!')
            return redirect('login')

        # Process the image using enhancement model
        enhanced_image_path = enhance_image(image)  # Call enhancement function

        # Save enhanced image in DB
        enhanced_image = EnhancedImage.objects.create(profile=profile, image=enhanced_image_path)
        messages.success(request, 'Image enhanced successfully!')
        latest_image = EnhancedImage.objects.filter(profile=profile).latest('created_at')

        return redirect('output-image', image_id=latest_image.id)
            
    return render(request, 'base/image_enhancement.html')
@login_required(login_url='login')
def delete_enhanced_image(request, image_id):
    """Handles image deletion by the authenticated user"""
    image = get_object_or_404(EnhancedImage, id=image_id)
    if not image:
        messages.error(request, 'Image does not exist!')

    # Ensure the user owns the image before deleting
    if request.user.profile == image.profile:
        image.delete()
        messages.success(request, 'Image was successfully deleted!')
    
    return redirect('profile', pk= request.user.id)

def imageColorization(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'User profile does not exist!')
            return redirect('login')

        if 'image' not in request.FILES:
            messages.error(request, 'No image file provided!')
            return redirect('image-colorization')

        image = request.FILES['image']
        profile = Profile.objects.get(user=request.user)
        if not profile:
            messages.error(request, 'User profile does not exist!')
            return redirect('login')

        # Process the image using colorization model
        colorized_image_path = colorize_image(image)  # Call colorization function

        # Save colorized image in DB
        colorized_image = ColorizedImage.objects.create(profile=profile, image=colorized_image_path)
        messages.success(request, 'Image colorized successfully!')
        latest_image = ColorizedImage.objects.filter(profile=profile).latest('created_at')

        return redirect('output-image', image_id=latest_image.id)
            
    return render(request, 'base/image_colorization.html')
@login_required(login_url='login')
def delete_colorized_image(request, image_id):
    """Handles image deletion by the authenticated user"""
    image = get_object_or_404(ColorizedImage, id=image_id)
    if not image:
        messages.error(request, 'Image does not exist!')

    # Ensure the user owns the image before deleting
    if request.user.profile == image.profile:
        image.delete()
        messages.success(request, 'Image was successfully deleted!')
    
    return redirect('profile', pk= request.user.id)

@login_required(login_url='login')
def outputImage(request, image_id= None):
    """
    Fetch and display the generated, enhanced, or colorized image based on the image_id.
    """
    image = None
    image_type = None

    if image_id:
        # Check in all models
        image = GeneratedImage.objects.filter(id=image_id).first()
        image_type = "Generated"

        if not image:
            image = EnhancedImage.objects.filter(id=image_id).first()
            image_type = "Enhanced"

        if not image:
            image = ColorizedImage.objects.filter(id=image_id).first()
            image_type = "Colorized"

    if not image:
        messages.error(request, 'Image not found!')
        return redirect('profile', pk=request.user.id)

    context = {'image': image, 'image_type': image_type}
    return render(request, 'base/output_image.html', context)
