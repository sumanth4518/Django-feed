from django.contrib import admin
from django.utils.html import format_html
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_snippet', 'image_thumbnail', 'created_at')
    list_display_links = ('id', 'content_snippet')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def content_snippet(self, obj):
        if not obj.content:
            return "[Image Only Post]"
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 40px; width: 40px; object-fit: cover; border-radius: 6px;" />', obj.image.url)
        return "-"
    image_thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = 'Uploaded Image Preview'
