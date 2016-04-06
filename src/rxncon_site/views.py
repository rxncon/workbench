from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# function based view, easier than class based but less strong



def rxncon_site_index(request):
    return render(request, "static_pages/index.html")
