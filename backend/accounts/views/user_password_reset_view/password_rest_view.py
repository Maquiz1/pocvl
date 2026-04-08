# accounts/views.py
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.conf import settings
from accounts.forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def get_email_context(self, user):
        context = super().get_email_context(user)
        context['protocol'] = getattr(settings, "PROTOCOL", "https")
        context['domain'] = getattr(settings, "DOMAIN_NAME", "logbook.apps.nimr.or.tz")
        return context