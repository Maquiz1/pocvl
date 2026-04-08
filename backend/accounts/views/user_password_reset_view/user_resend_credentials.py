
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
