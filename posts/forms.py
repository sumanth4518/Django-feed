from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts.
    """
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg post-content-textarea',
            'rows': 4,
            'placeholder': "What's happening? Share something with the community...",
            'id': 'id_content'
        }),
        label="Post Content"
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/webp,image/jpg,image/gif',
            'id': 'post-image-input'
        }),
        label="Upload Image (Optional)"
    )

    class Meta:
        model = Post
        fields = ['content', 'image']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content', '').strip()
        image = cleaned_data.get('image')

        # If editing an existing post that already has an image and no new image is provided
        has_existing_image = bool(self.instance and self.instance.pk and self.instance.image)

        if not content and not image and not has_existing_image:
            raise ValidationError("Please provide either text content or an image for your post.")

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate max file size (10MB)
            if hasattr(image, 'size') and image.size > 10 * 1024 * 1024:
                raise ValidationError("Image file size cannot exceed 10MB.")

            # Validate extension
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
            if not image.name.lower().endswith(valid_extensions):
                raise ValidationError("Unsupported image format. Allowed formats: JPG, JPEG, PNG, WEBP, GIF.")

        return image
