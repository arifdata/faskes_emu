from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_page(request):
    context = {'nama': 'User', 'data': [25, 40, 30, 35, 8, 52, 17, -4]}
    return render(request, 'pendaftaran/index.html', context)