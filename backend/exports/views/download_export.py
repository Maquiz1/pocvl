from django.http import FileResponse
import os

def download_export(request, path):
    return FileResponse(open(path, "rb"), as_attachment=True)