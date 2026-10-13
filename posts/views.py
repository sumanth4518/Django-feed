from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Post
from .forms import PostForm


def home_view(request):
    """
    Landing page for visitors.
    If authenticated, redirects directly to user feed.
    """
    if request.user.is_authenticated:
        return redirect('feed')
    
    # Showcase latest 3 public posts on the landing page for demonstration
    recent_posts = Post.objects.select_related('user', 'user__profile').order_by('-created_at')[:3]
    return render(request, 'home.html', {'recent_posts': recent_posts})


@login_required
def feed_view(request):
    """
    Main feed view showing latest posts from all users with quick-post support.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been published successfully!")
            return redirect('feed')
        else:
            messages.error(request, "Unable to publish post. Please check the errors below.")
    else:
        form = PostForm()

    posts = Post.objects.select_related('user', 'user__profile').order_by('-created_at')
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'form': form,
    })


@login_required
def post_create_view(request):
    """
    Dedicated page for creating a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('feed')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form': form})


def post_detail_view(request, pk):
    """
    Detailed single post view.
    """
    post = get_object_or_404(Post.objects.select_related('user', 'user__profile'), pk=pk)
    is_owner = request.user.is_authenticated and (request.user == post.user)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'is_owner': is_owner,
    })


@login_required
def post_edit_view(request, pk):
    """
    Edit an existing post. Only the owner can edit.
    """
    post = get_object_or_404(Post, pk=pk)

    # Strict authorization check
    if post.user != request.user:
        messages.error(request, "You are not authorized to edit this post.")
        raise PermissionDenied("You cannot edit a post that does not belong to you.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        
        # Check if user checked the 'remove_image' option
        if request.POST.get('remove_image') == 'true' and post.image:
            post.image.delete(save=False)
            post.image = None

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_edit.html', {
        'form': form,
        'post': post,
    })


@login_required
def post_delete_view(request, pk):
    """
    Delete a post with confirmation. Only the owner can delete.
    """
    post = get_object_or_404(Post, pk=pk)

    # Strict authorization check
    if post.user != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        raise PermissionDenied("You cannot delete a post that does not belong to you.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('feed')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})
