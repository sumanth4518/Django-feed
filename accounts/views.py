from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register_view(request):
    """
    Handles user registration. Automatically creates user and profile,
    then signs them in and redirects to the feed.
    """
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome aboard, @{user.username}! Your account has been created successfully.")
            return redirect('feed')
        else:
            messages.error(request, "Please correct the errors below to register.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handles user login authentication.
    """
    if request.user.is_authenticated:
        return redirect('feed')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, @{user.username}!")
                
                # Check redirect security
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('feed')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """
    Logs out the current authenticated user and redirects to home page.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully. See you soon!")
    return redirect('home')


@login_required
def my_profile_view(request):
    """
    Redirects authenticated user to their own public profile page.
    """
    return redirect('profile', username=request.user.username)


def profile_view(request, username):
    """
    Displays a user's public profile and their list of posts.
    Accessible to both guests and logged-in users.
    """
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    user_posts = profile_user.posts.all().order_by('-created_at')
    
    is_owner = request.user.is_authenticated and (request.user == profile_user)

    context = {
        'profile_user': profile_user,
        'profile': profile_user.profile,
        'posts': user_posts,
        'posts_count': user_posts.count(),
        'is_owner': is_owner,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Allows the logged-in user to update their account information
    (first name, last name, email) and profile details (bio, avatar).
    """
    # Ensure profile exists for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user, user=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please fix the errors below before saving your profile.")
    else:
        user_form = UserUpdateForm(instance=request.user, user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
