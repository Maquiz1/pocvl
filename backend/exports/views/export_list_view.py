from django.shortcuts import render


def export_list_view(request):
    context = {
        "title": "Export Data",
    }


    return render(
        request,
        "exports/export_list.html",
        context
    )
    