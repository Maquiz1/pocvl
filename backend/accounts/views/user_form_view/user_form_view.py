
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
    
    subject = "Your Herbal Trial Credentials"
    user = User.objects.get(email=email)
    html_message = render_to_string('registration/credential_email.html', {
        'email': email,
        'password': password,
        'login_url': login_url,
        'user': user
    })
    
    send_mail(
        subject=subject,
        message=f"Hello,\n\nYour account has been created/updated.\nEmail: {email}\nPassword: {password}\nLogin at: {login_url}",
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
