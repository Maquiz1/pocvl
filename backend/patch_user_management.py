import re
import os

# 1. Update accounts/forms.py
forms_path = 'accounts/forms.py'
with open(forms_path, 'r') as f:
    forms_obj = f.read()

# Strip lines 170 to end
forms_lines = forms_obj.splitlines()

# We will cut off the massive commented out section starting at `# class StaffForm(forms.Form):`
# and replace it with the clean version.
new_forms = []
for line in forms_lines:
    if line.strip().startswith('# class StaffForm(forms.Form):'):
        break
    new_forms.append(line)

new_form_code = """
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
"""

with open(forms_path, 'w') as f:
    f.write("\n".join(new_forms) + "\n" + new_form_code)


# 2. Update accounts/views/user_form_view.py
form_view_path = 'accounts/views/user_form_view/user_form_view.py'
new_form_view_code = """
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.models import StaffProfile
from accounts.forms import StaffForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()

def send_credentials_email(email, password, request):
    protocol = getattr(settings, 'PROTOCOL', 'https')
    domain = getattr(settings, 'DOMAIN_NAME', 'logbook.apps.nimr.or.tz')
    login_url = f"{protocol}://{domain}/accounts/login/"
    
    subject = "Your Logbook Credentials"
    html_message = render_to_string('registration/credential_email.html', {
        'email': email,
        'password': password,
        'login_url': login_url
    })
    
    send_mail(
        subject=subject,
        message=f"Hello,\\n\\nYour account has been created/updated.\\nEmail: {email}\\nPassword: {password}\\nLogin at: {login_url}",
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@nimr.or.tz'),
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message
    )


class StaffCreateUpdateView(FormView):
    template_name = "users/staff/staff_form.html"
    form_class = StaffForm
    success_url = reverse_lazy("accounts:staff_list")

    def dispatch(self, request, *args, **kwargs):
        self.user_instance = None
        pk = kwargs.get("pk")
        if pk:
            self.user_instance = get_object_or_404(User, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.user_instance:
            initial.update({
                "email": self.user_instance.email,
                "first_name": self.user_instance.first_name,
                "last_name": self.user_instance.last_name,
                "is_active": self.user_instance.is_active,
                "is_staff": self.user_instance.is_staff,
                "groups": self.user_instance.groups.all(),
            })
            if hasattr(self.user_instance, "staff_profile"):
                profile = self.user_instance.staff_profile
                initial.update({
                    "middle_name": getattr(profile, "middle_name", ""),
                    "prefix": profile.prefix,
                    "position": profile.position,
                    "site": profile.site,
                    "phone": profile.phone,
                    "role": profile.role,
                })
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.user_instance:
            form.instance = self.user_instance
        return form

    def form_valid(self, form):
        data = form.cleaned_data
        password = data.get("password")
        email = data.get("email")
        first_name = data.get("first_name")
        middle_name = data.get("middle_name")
        last_name = data.get("last_name")
        prefix = data.get("prefix")
        position = data.get("position")
        site = data.get("site")
        phone = data.get("phone")
        role = data.get("role")
        is_active = data.get("is_active", True)
        is_staff = data.get("is_staff", True)
        groups = data.get("groups")

        is_new = self.user_instance is None
        user = self.user_instance

        if not user:
            user = User(email=email)
        else:
            user.email = email

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_active = is_active
        
        credentials_sent = False
        if password:
            user.set_password(password)
        elif is_new:
            password = User.objects.make_random_password()
            user.set_password(password)
            send_credentials_email(email, password, self.request)
            credentials_sent = True
            
        user.save()

        profile, _ = StaffProfile.objects.get_or_create(user=user)
        profile.middle_name = middle_name
        profile.prefix = prefix
        profile.position = position
        profile.site = site
        profile.phone = phone
        profile.role = role
        profile.save()
        
        if groups is not None:
            user.groups.set(groups)
            
        if is_new:
            if not credentials_sent:
                # If password was provided, still send an email so they have their link
                try:
                    send_credentials_email(email, password, self.request)
                except Exception as e:
                    pass
            messages.success(self.request, f"Staff member '{email}' created successfully! Credentials emailed.")
        else:
            messages.success(self.request, f"Staff member '{email}' updated successfully!")

        return super().form_valid(form)
"""
with open(form_view_path, 'w') as f:
    f.write(new_form_view_code)


# 3. Update accounts/views/user_list_view.py
list_view_path = 'accounts/views/user_list_view/user_list_view.py'
new_list_view_code = """
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from accounts.models import Prefix, Position
from herbal.models import Site
from django.contrib.auth.models import Group
from django.db.models import Q

User = get_user_model()

class StaffListView(ListView):
    model = User
    template_name = 'users/staff/staff_list.html'
    context_object_name = 'staff_list'
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.all().select_related(
            'staff_profile',
            'staff_profile__position',
        ).prefetch_related('groups').order_by('email')

        full_name = self.request.GET.get('full_name')
        email = self.request.GET.get('email')
        prefix = self.request.GET.get('prefix')
        position = self.request.GET.get('position')
        site = self.request.GET.get('site')
        group = self.request.GET.get('group')

        if full_name:
            qs = qs.filter(Q(first_name__icontains=full_name) | Q(last_name__icontains=full_name))
        if email:
            qs = qs.filter(email__icontains=email)
        if prefix:
            qs = qs.filter(staff_profile__prefix_id=prefix)
        if position:
            qs = qs.filter(staff_profile__position_id=position)
        if site:
            qs = qs.filter(staff_profile__site_id=site)
        if group:
            qs = qs.filter(groups__id=group)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefixes'] = Prefix.objects.all()
        context['positions'] = Position.objects.all()
        context['sites'] = Site.objects.all()
        context['groups'] = Group.objects.all()
        return context
"""
with open(list_view_path, 'w') as f:
    f.write(new_list_view_code)

# 4. Create resend credentials view
resend_view_path = 'accounts/views/user_password_reset_view/user_resend_credentials.py'
new_resend_code = """
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.views.user_form_view.user_form_view import send_credentials_email

User = get_user_model()

def resend_credentials_view(request, pk):
    if request.method == "POST":
        user = get_object_or_404(User, pk=pk)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        
        try:
            send_credentials_email(user.email, password, request)
            messages.success(request, f"New credentials generated & sent to {user.email}.")
        except Exception as e:
            messages.error(request, f"Failed to send email to {user.email}: {e}")
            
    return redirect('accounts:staff_list')
"""
with open(resend_view_path, 'w') as f:
    f.write(new_resend_code)

print("Backend rewrite complete.")
