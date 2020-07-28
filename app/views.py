from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request, 'base.html')

def search(request):
    input_search = request.POST.get('search')
    print(input_search)
    return render(request, 'search.html', {'input_search': input_search})
