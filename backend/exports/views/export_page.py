from django.shortcuts import render

def export_page(request):
    return render(request, "exports/export.html")