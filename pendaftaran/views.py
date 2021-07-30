from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_page(request):
    html = """
    <h1>Welcome</h1>
    <a href='app/'>Login Ke App</a>
    """
    return HttpResponse(html)