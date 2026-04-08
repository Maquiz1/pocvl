# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import AuthenticationForm
# from django.urls import reverse_lazy, reverse
# from django.utils.html import format_html
# from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
# from phonenumber_field.formfields import PhoneNumberField
# from accounts.models import Profile, Prefix, Position, Site
# from django.contrib.auth.models import Group
# from phonenumbers import parse, is_valid_number, NumberParseException
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
# import re

# User = get_user_model()

# # users/forms.py
# from django import forms
# from django.contrib.auth import get_user_model
# from .models import Profile, Prefix, Position

# User = get_user_model()

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['site', 'phone_number', 'prefix', 'position']
#         widgets = {
#             'site': forms.Select(attrs={'class': 'form-select'}),
#             'prefix': forms.Select(attrs={'class': 'form-select'}),
#             'position': forms.Select(attrs={'class': 'form-select'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )

    error_messages = {
        "invalid_login": "Invalid email or password",
        "inactive": "This account is inactive",
    }

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password
            )
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Username',
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Password',
#         })
#     )

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         if username and password:
#             UserModel = get_user_model()
#             try:
#                 user = UserModel.objects.get(username=username)

#                 if not user.is_active:
#                     resend_url = reverse_lazy('users:resend_activation')
#                     raise forms.ValidationError(
#                         format_html(
#                             'Your account is inactive. <a href="{}">Resend activation email</a>',
#                             resend_url
#                         ),
#                         code='inactive'
#                     )

#                 # Only authenticate if user is active
#                 user = authenticate(self.request, username=username, password=password)
#                 if user is None:
#                     raise forms.ValidationError(
#                         "Invalid username or password.",
#                         code='invalid_login'
#                     )

#                 # ✅ Required: Store the user in self.user_cache (what AuthenticationForm expects)
#                 self.user_cache = user

#             except UserModel.DoesNotExist:
#                 raise forms.ValidationError(
#                     "Invalid username or password.",
#                     code='invalid_login'
#                 )

#         return self.cleaned_data

#     def get_user(self):
#         return getattr(self, 'user_cache', None)
    
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     phone_number = forms.CharField(max_length=15)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email__iexact=email).exists():
#             raise forms.ValidationError("This email address is already registered.")
#         return email

# class ResendActivationEmailForm(forms.Form):
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
#     )
    
class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

# class PhoneVerificationForm(forms.Form):
#     phone_number = PhoneNumberField(region="TZ")  # or your default region code
    
    
    

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import StaffProfile, Prefix, Position
from herbal.models import Site

User = get_user_model()

class StaffForm(forms.Form):
    # User fields
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        required=False,
        label="Password (leave blank to auto-generate)",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    middle_name = forms.CharField(
        max_length=150,
        required=False,
        label="Middle Name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    is_active = forms.BooleanField(
        required=False,
        label="Is Active",
        initial=True,
        widget=forms.CheckboxInput()
    )
        
    is_staff = forms.BooleanField(
        required=False,
        label="Is Staff",
        initial=False,
        widget=forms.CheckboxInput()
    )

    # Profile fields
    role = forms.ChoiceField(
        choices=[("", "---------")] + [
            ("admin", "Admin"),
            ("data_manager", "Data Manager"),
            ("monitor", "Monitor"),
            ("coordinator", "Coordinator"),
            ("data_clerk", "Data Clerk"),
            ("reviewer", "Reviewer"),
            ("pi", "Principal Investigator"),
        ],
        required=True,
        label="Role",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    prefix = forms.ModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label="Prefix",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="Position",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label="Site",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            qs = User.objects.filter(email__iexact=email)
            if getattr(self, "instance", None):
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("This email address is already registered.")
        return email
