"""
Seed Script for SocialApp
Creates sample users and demo posts with images to quickly test the application.
Usage:
    python seed_demo.py
"""

import os
import sys
import io
from pathlib import Path
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_app.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post
from accounts.models import Profile


def generate_banner_image(text, bg_color=(79, 70, 229)):
    """Generate a simple banner image for demo posts."""
    width, height = 800, 450
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Simple accent shapes
    draw.rectangle([0, height - 20, width, height], fill=(124, 58, 237))
    file = io.BytesIO()
    img.save(file, format='JPEG', quality=90)
    file.seek(0)
    return file.getvalue()


def seed():
    print("Seeding SocialApp demo data...")

    # 1. Create or get Admin
    admin_user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Super',
        'last_name': 'Admin'
    })
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.profile.bio = "System Administrator for SocialApp."
        admin_user.profile.save()
        print("  [OK] Created superuser: admin (password: admin123)")
    else:
        print("  * Superuser 'admin' already exists.")

    # 2. Create sample creator users
    users_data = [
        {
            'username': 'sumanth',
            'first_name': 'Sumanth',
            'last_name': 'Reddy',
            'email': 'sumanth@example.com',
            'bio': 'Software Engineer & Django enthusiast. Passionate about building clean web applications.'
        },
        {
            'username': 'sarah_creator',
            'first_name': 'Sarah',
            'last_name': 'Jenkins',
            'email': 'sarah@example.com',
            'bio': 'Travel photographer and UI/UX designer exploring the world one city at a time.'
        },
        {
            'username': 'david_dev',
            'first_name': 'David',
            'last_name': 'Chen',
            'email': 'david@example.com',
            'bio': 'Full-stack builder passionate about open source and scalable backend architectures.'
        }
    ]

    created_users = []
    for udata in users_data:
        u, created = User.objects.get_or_create(username=udata['username'], defaults={
            'email': udata['email'],
            'first_name': udata['first_name'],
            'last_name': udata['last_name']
        })
        if created:
            u.set_password('password123')
            u.save()
            u.profile.bio = udata['bio']
            u.profile.save()
            print(f"  [OK] Created user: @{u.username} (password: password123)")
        else:
            print(f"  * User @{u.username} already exists.")
        created_users.append(u)

    # 3. Create Sample Posts
    sumanth = created_users[0]
    sarah = created_users[1]
    david = created_users[2]

    if not Post.objects.filter(user=sumanth).exists():
        p1 = Post.objects.create(
            user=sumanth,
            content="Welcome to SocialApp! This application is built with Django, MySQL, and clean responsive UI. Feel free to create your own posts and upload images."
        )
        print(f"  [OK] Created post by @{sumanth.username}")

    if not Post.objects.filter(user=sarah).exists():
        img_bytes = generate_banner_image("Golden Sunset Views", bg_color=(234, 88, 12))
        img_file = SimpleUploadedFile("sunset.jpg", img_bytes, content_type="image/jpeg")
        p2 = Post.objects.create(
            user=sarah,
            content="Golden hour over the skyline. Capturing moments like this is why I love photography!",
            image=img_file
        )
        print(f"  [OK] Created image post by @{sarah.username}")

    if not Post.objects.filter(user=david).exists():
        p3 = Post.objects.create(
            user=david,
            content="Just pushed an update to our new architecture! Clean separation of concerns makes building in Django a breeze."
        )
        print(f"  [OK] Created post by @{david.username}")

    print("\nSeeding complete! You can now log in with:")
    print("   Username: sumanth / Password: password123")
    print("   Username: sarah_creator / Password: password123")
    print("   Username: admin / Password: admin123\n")


if __name__ == '__main__':
    seed()
