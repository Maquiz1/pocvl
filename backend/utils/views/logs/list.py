from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from utils.models import EmailLog


@login_required
def email_logs_dashboard(request):
    logs = EmailLog.objects.all().order_by('-created_at')

    # 🔎 Search
    search_query = request.GET.get('search')
    if search_query:
        logs = logs.filter(
            Q(recipient__icontains=search_query) |
            Q(subject__icontains=search_query)
        )

    # 📅 Date range filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        logs = logs.filter(created_at__date__gte=start_date)

    if end_date:
        logs = logs.filter(created_at__date__lte=end_date)

    # Optional status filter (keep your existing logic)
    status = request.GET.get('status')
    if status:
        logs = logs.filter(status=status)

    # 📄 Pagination
    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total": logs.count(),
        "sent_count": logs.filter(status="sent").count(),
        "failed_count": logs.filter(status="failed").count(),
        "search_query": search_query,
        "start_date": start_date,
        "end_date": end_date,
        "status": status,
    }

    return render(request, "utils/logs/email_logs.html", context)