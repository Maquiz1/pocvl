from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import EmailRecipient

class EmailRecipientListView(ListView):
    model = EmailRecipient
    template_name = "utils/email_recipients/list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        # Only show non-deleted recipients
        return EmailRecipient.objects.filter(is_deleted=False)


class EmailRecipientCreateView(CreateView):
    model = EmailRecipient
    fields = ["email", "type", "is_active"]
    template_name = "utils/email_recipients/add.html"
    success_url = reverse_lazy("utils:email_recipient_list")


class EmailRecipientUpdateView(UpdateView):
    model = EmailRecipient
    fields = ["email", "type", "is_active"]
    template_name = "utils/email_recipients/edit.html"
    success_url = reverse_lazy("utils:email_recipient_list")


class EmailRecipientDeleteView(DeleteView):
    model = EmailRecipient
    template_name = "utils/email_recipients/delete.html"
    success_url = reverse_lazy("utils:email_recipient_list")

    def delete(self, request, *args, **kwargs):
        """Soft delete instead of removing from DB."""
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.save(update_fields=["is_deleted", "is_active"])
        return super().delete(request, *args, **kwargs)
