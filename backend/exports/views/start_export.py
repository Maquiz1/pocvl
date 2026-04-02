from django.http import JsonResponse
from ..tasks import export_data_task

def start_export(request):
    task = export_data_task.delay()
    return JsonResponse({"task_id": task.id})