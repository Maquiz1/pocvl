import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

from django.test import RequestFactory
from accounts.forms import CustomPasswordResetForm

print("\nTesting CustomPasswordResetForm:")
rf = RequestFactory()
request = rf.post('/password_reset/', {'email': 'manquiz92@gmail.com'}, HTTP_HOST='127.0.0.1')

form = CustomPasswordResetForm({"email": "manquiz92@gmail.com"})
if form.is_valid():
    try:
        form.save(
            use_https=False,
            email_template_name='registration/password_reset_email.txt',
            html_email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            from_email="noreply@test.com",
            request=request,
            extra_email_context={}
        )
        print("Password reset form processed successfully.")
    except Exception as e:
        print(f"Error in form.save: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Form invalid:", form.errors)
