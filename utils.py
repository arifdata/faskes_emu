from django.http import FileResponse

def download_backup(request):
    return FileResponse(open('db.sqlite3', 'rb'), as_attachment=True)
