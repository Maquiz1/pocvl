import os
import re

files_to_update = [
    "accounts/views/user_form_view/user_form_view.py",
    "accounts/templates/registration/password_reset_email.txt",
    "accounts/templates/registration/password_reset_subject.txt",
    "accounts/templates/registration/password_reset_email.html",
    "accounts/templates/registration/password_reset_done.html",
    "accounts/templates/registration/credential_email.html",
    "accounts/templates/registration/password_reset_complete.html",
    "accounts/templates/registration/password_reset_form.html",
]

for filepath in files_to_update:
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()

        # Replace text, but carefully avoid logbook.apps URLs
        # "LogBook" -> "Herbal Trial"
        content = content.replace("LogBook", "Herbal Trial")
        # "Logbook" -> "Herbal Trial" (skipping the lowercase ones that might be in URLs unless there's a space or capital L)
        content = content.replace("Your Logbook", "Your Herbal Trial")
        content = content.replace("Back to Logbook", "Back to Herbal Trial")
        content = content.replace("back Logbook", "back to Herbal Trial")
        content = content.replace("- LogBook", "- Herbal Trial")
        content = content.replace("Reset Password - Logbook", "Reset Password - Herbal Trial")
        
        with open(filepath, "w") as f:
            f.write(content)
            
print("Renamed 'Logbook' to 'Herbal Trial' in templates and emails.")
