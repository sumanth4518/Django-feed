from django.shortcuts import render


def custom_404_view(request, exception=None):
    """Custom 404 Not Found error page."""
    return render(request, 'errors/404.html', status=404)


def custom_403_view(request, exception=None):
    """Custom 403 Forbidden / Permission Denied error page."""
    return render(request, 'errors/403.html', {'exception': exception}, status=403)


def custom_500_view(request):
    """Custom 500 Internal Server Error page."""
    return render(request, 'errors/500.html', status=500)
