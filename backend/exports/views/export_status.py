from celery.result import AsyncResult
from django.http import JsonResponse

def export_status(request, task_id):
    task = AsyncResult(task_id)

    if task.state == "PENDING":
        return JsonResponse({"status": "PENDING", "progress": 0})

    elif task.state == "PROGRESS":
        return JsonResponse({
            "status": "PROGRESS",
            "progress": task.info.get("progress", 0)
        })

    elif task.state == "SUCCESS":
        return JsonResponse({
            "status": "SUCCESS",
            "progress": 100,
            "file": task.result.get("file")
        })

    else:
        return JsonResponse({"status": "FAILED", "progress": 0})