from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_page(request):
    context = {'nama': 'User'}
    return render(request, 'pendaftaran/index.html', context)