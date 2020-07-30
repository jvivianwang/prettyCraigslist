import calendar
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests.utils import requote_uri
from . import models

# Create your views here.
BASE_CRAIGSLIST_URL = "https://atlanta.craigslist.org/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

def search(request):
    input_search = request.POST.get('search')
    # add search strings in the db
    models.Search.objects.create(search = input_search)
    encode_search = requote_uri(input_search)
    final_url = BASE_CRAIGSLIST_URL.format(encode_search)
    response = requests.get(final_url)
    soup = BeautifulSoup(response.text, features='html.parser')
    data = soup.findAll("li", {"class" : "result-row"})
    final_listing =[]

    for d in data:
        # name
        data_name = d.find(class_='result-title hdrlnk').text
        # url
        data_url = d.find(class_='result-title hdrlnk').get('href')
        # date
        data_date = d.find(class_='result-date').get('datetime').split()[0]
        data_date = data_date.replace('-', ' ')[5:]
        month = int(data_date[0:2])
        date = data_date[3:5]
        data_date = calendar.month_name[month] + " " + date
        # image
        if d.find(class_='result-image').get('data-ids'):
            data_image_id = d.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            data_image_url = BASE_IMAGE_URL.format(data_image_id)

        else:
            data_image_url = 'https://craigslist.org/images/peace.jpg'

        # price
        if d.find(class_='result-price'):
            data_price = d.find(class_='result-price').text
        else:
            data_price = 'N/A'

        final_listing.append((data_name, data_url, data_date, data_price, data_image_url))


    return render(request, 'search.html', {'input_search': input_search, 'final_listing': final_listing})
