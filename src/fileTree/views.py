from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import File
#from .forms import FileForm

# def file_list(request):  moved to context processor
#     # queryset_list = File.objects.all()
#     queryset_list = File.objects.all().order_by("slug")
#     slug_list = list(set([File.get_project_slug() for File in queryset_list])) # list(set()) to get unique values
#     projects= [queryset_list.filter(slug=slug).order_by("-timestamp") for slug in slug_list]
#
#
#
#     # paginator = Paginator(queryset_list, 10)
#     # page_request_var= "page"
#     # page = request.GET.get('page_request_var')
#     # try:
#     #     queryset = paginator.page(page)
#     # except PageNotAnInteger:
#     #     # If page is not an integer, deliver first page.
#     #     queryset = paginator.page(1)
#     # except EmptyPage:
#     #     # If page is out of range (e.g. 9999), deliver last page of results.
#     #     queryset = paginator.page(paginator.num_pages)
#
#     context_data = {
#         # "object_list":queryset,
#         "object_list":queryset_list,
#         "title":"Projects",
#         "slug_list": slug_list,
#         "projects": projects,
#         # "page_request_var":page_request_var,
#     }
#
#     return render(request, "file_list.html", context_data)

def file_detail(request, slug=None):
    # instance = get_object_or_404(File, slug=slug)
    project_files = File.objects.filter(slug=slug)
    instance = project_files.latest("updated")
    context_data = {
        "project_files":project_files,
        "title": instance.project_name,
        "instance":instance,
    }
    return render(request, "file_detail.html", context_data)

# def get_slug_dir_list(dict_list):
#     return [dict["slug"] for  dict in dict_list]
#     # slug_set = set(queryset_list.slug)
#     # return list(slug_set)