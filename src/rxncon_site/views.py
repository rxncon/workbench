from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# function based view, easier than class based but less strong



def rxncon_site_index(request):
    return render(request, "static_pages/index.html")

def publications(request):
    return render(request, "static_pages/publications.html")

def funding(request):
    return render(request, "static_pages/funding.html")

def support(request):
    return render(request, "static_pages/support.html")

def guided_tour(request):
    return render(request, "guided_tour.html")
