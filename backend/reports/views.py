from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from herbal.models.enrollments.enrollment_model import Enrollment
from herbal.models.visits.visit_schedule_model import VisitSchedule
from sites.models import Site

@login_required
def monthly_report(request):
    today = timezone.now().date()
    site_id = request.GET.get('site')
    month_filter = request.GET.get('month')
    sites = Site.objects.all()

    enrollments_qs = Enrollment.objects.all()
    visits_qs = VisitSchedule.objects.all()

    if site_id:
        enrollments_qs = enrollments_qs.filter(screening__subject__site_id=site_id)
        visits_qs = visits_qs.filter(enrollment__screening__subject__site_id=site_id)

    if month_filter:
        try:
            year, month = month_filter.split('-')
            enrollments_qs = enrollments_qs.filter(enrollment_date__year=int(year), enrollment_date__month=int(month))
            visits_qs = visits_qs.filter(scheduled_date__year=int(year), scheduled_date__month=int(month))
        except (ValueError, TypeError):
            pass

    enrollment_stats = enrollments_qs.annotate(
        month=TruncMonth('enrollment_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')

    visit_stats = visits_qs.annotate(
        month=TruncMonth('scheduled_date')
    ).values('month').annotate(
        expected=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        attended=Count('id', filter=Q(status__in=['completed', 'incomplete'])),
        missed=Count('id', filter=Q(status='missed')),
        overdue=Count('id', filter=Q(status='pending', scheduled_date__lt=today)),
        pending=Count('id', filter=Q(status='pending', scheduled_date__gte=today)),
    ).order_by('-month')

    # Create properly formatted data for Chart.js (reverse so oldest month is first)
    enrollment_data = []
    # enrollment_stats is a QuerySet, we reverse it locally because it is ordered by -month
    for stat in reversed(list(enrollment_stats)):
        enrollment_data.append({
            'month': stat['month'].strftime('%b %Y') if stat['month'] else 'Unknown',
            'count': stat['count']
        })
    
    visit_data = []
    for stat in reversed(list(visit_stats)):
        visit_data.append({
            'month': stat['month'].strftime('%b %Y') if stat['month'] else 'Unknown',
            'expected': stat['expected'],
            'attended': stat['attended'],
            'completed': stat['completed'],
            'missed': stat['missed'],
            'pending': stat['pending'],
            'overdue': stat['overdue']
        })

    # Data for Per-Site Charts
    site_stats_enrollment = enrollments_qs.values('screening__subject__site__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    site_data_enrollment = []
    for stat in site_stats_enrollment:
        site_data_enrollment.append({
            'site': stat['screening__subject__site__name'] or 'Unknown',
            'count': stat['count']
        })
        
    site_stats_visits = visits_qs.values('enrollment__screening__subject__site__name').annotate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed'))
    ).order_by('-total')
    
    site_data_visits = []
    for stat in site_stats_visits:
        site_data_visits.append({
            'site': stat['enrollment__screening__subject__site__name'] or 'Unknown',
            'total': stat['total'],
            'completed': stat['completed']
        })

    context = {
        'sites': sites,
        'selected_site': site_id,
        'selected_month': month_filter,
        'enrollment_stats': enrollment_stats,
        'visit_stats': visit_stats,
        'enrollment_chart_data': enrollment_data,
        'visit_chart_data': visit_data,
        'site_enrollment_chart_data': site_data_enrollment,
        'site_visit_chart_data': site_data_visits,
    }
    return render(request, 'reports/monthly_report.html', context)
