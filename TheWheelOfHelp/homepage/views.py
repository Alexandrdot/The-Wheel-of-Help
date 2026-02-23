from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.

def error_404(request, exception):
    return HttpResponseNotFound("Error 404")


def index(request):
    return HttpResponse('HomePage')


def technical_service_station(request):
    return HttpResponse('СТО')


def evacuator(request):
    name = request.GET.get('name')
    return HttpResponse(f'Эвакуаторы и {name}')


def tire_service(request):
    return HttpResponse('Шиномонтаж')


def search(request):
    return redirect('homepage:index')


def open_tech_station(request, id):
    return HttpResponse(f'СТО {id}')


def open_evacuator(request, id):
    return HttpResponse(f'Эвакуатор {id}')


def open_tire_service(request, id):
    return HttpResponse(f'Шиномонтаж {id}')


def rating(request, rating):
    if rating >= 4.8:
        category = "Отличный"
    elif rating >= 4.0:
        category = "Хороший"
    elif rating >= 3.0:
        category = "Неплохой"
    elif rating >= 2.0:
        category = "Средний"
    else:
        category = "Плохой" # Edit this

    return HttpResponse(f"<h1>{category}<h1>")

