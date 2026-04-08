import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

from django.core.mail import send_mail
from accounts.forms import CustomPasswordResetForm

print("Testing direct send_mail:")
try:
    send_mail("Subject here", "Here is the message.", "from@example.com", ["to@example.com"])
    print("Direct send_mail complete.")
except Exception as e:
    print(f"Error in send_mail: {e}")

print("\nTesting CustomPasswordResetForm:")
form = CustomPasswordResetForm({"email": "manquiz92@gmail.com"})
if form.is_valid():
    try:
        form.save(
            use_https=False,
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            from_email="noreply@test.com",
            request=None,
        )
        print("Password reset form processed successfully.")
    except Exception as e:
        print(f"Error in form.save: {e}")
else:
    print("Form invalid:", form.errors)
