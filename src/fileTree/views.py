from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import rxncon.input.excel_book.excel_book as rxncon_excel


from .models import File
from .forms import FileForm, DeleteFileForm

def file_list(request):  #moved to context processor
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
    pass

def file_detail(request, slug=None):
    # instance = get_object_or_404(File, slug=slug)
    project_files = File.objects.filter(slug=slug)
    instance = project_files.latest("updated")
    # book= rxncon_excel.ExcelBookWithReactionType(instance.get_absolute_path())
    # rxncon_system = book.rxncon_system

    context_data = {
        "project_files":project_files,
        "title": instance.project_name,
        "instance":instance,
        # "book":book,
        # "nr_reactions":len(rxncon_system.reactions),
        "nr_reactions":"currently deactivated in fileTree/views.py",
    }
    return render(request, "file_detail.html", context_data)


def file_upload(request, slug= None):
    # TODO: like this, it is not case sensitive. "Elefant" and "elefant" are the same project
    form = FileForm(request.POST or None, request.FILES or None)
    if slug != None:
        try:
            file= File.objects.filter(slug=slug)[0]
            project_name= file.project_name
            form = FileForm(initial={'project_name':project_name })
        except KeyError:
            pass

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        "form": form,
    }
    return render(request, "file_form.html", context)

def file_delete(request, id):
    f = get_object_or_404(File, id=id)
    project_name= f.project_name
    updated= f.updated
    timestamp= f.timestamp

    if request.method == 'POST':
        form = DeleteFileForm(request.POST, instance=f)

        if form.is_valid(): # checks CSRF
            f.delete()
            return HttpResponseRedirect("/") # wherever to go after deleting

    else:
        form = DeleteFileForm(instance=f)

    template_vars = {'form': form,
                     'project_name': project_name,
                     "updated": updated,
                     "timestamp": timestamp,}
    return render(request, 'file_delete.html', template_vars)