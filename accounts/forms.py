from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.ModelForm):
    """
    Registration form with username, email, password, and confirm password fields.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'autocomplete': 'email',
        }),
        help_text="A valid email address is required."
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter strong password',
            'autocomplete': 'new-password',
        }),
        help_text="Password must be at least 6 characters long."
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        }),
        help_text="Re-enter the password exactly as above."
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a unique username',
                'autocomplete': 'username',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with that username already exists. Please pick another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match. Please verify and try again.")
            elif len(password) < 6:
                self.add_error('password', "Password must be at least 6 characters long.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Styled login form for username and password authentication.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user account information (First name, Last name, Email).
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.user:
            duplicate = User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists()
            if duplicate:
                raise ValidationError("This email address is already in use by another account.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information (Bio and Profile Picture).
    """
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a brief bio about yourself...',
                'maxlength': '500',
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp,image/jpg',
                'id': 'profile-image-input',
            }),
        }

    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')
        if image:
            # Check file size (limit to 5MB)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise ValidationError("Profile picture size cannot exceed 5MB.")

            # Validate file extension
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            if not image.name.lower().endswith(valid_extensions):
                raise ValidationError("Unsupported file format. Please upload JPG, JPEG, PNG, or WEBP.")
        return image
