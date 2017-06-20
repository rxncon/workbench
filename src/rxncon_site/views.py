from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from fileTree.models import File
from quick_format.models import Quick
from rxncon_system.models import Rxncon_system
import rxncon.input.quick.quick as rxncon_quick
import rxncon.input.excel_book.excel_book as rxncon_excel
import pickle


# function based view, easier than class based but less strong



def rxncon_site_index(request):
    return render(request, "static_pages/index.html")

def publications(request):
    return render(request, "static_pages/publications.html")

def funding(request):
    return render(request, "static_pages/funding.html")

def support(request):
    return render(request, "static_pages/support.html")

def compare_systems(request, id, system, called_from="File"):
    rxncon_system = system#.rxncon_system

    rxns = 0
    for rxn in rxncon_system.reactions:
        if not rxn in system.reactions:
            rxns +=1

    cnts = 0
    for cnt in rxncon_system.contingencies:
        if not cnt in system.contingencies:
            cnts += 1

    return {"rxns": rxns,
            "cnts": cnts}

def getting_started(request):
    return render(request, "getting_started.html")

def create_rxncon_system(request, system_type, system_id):
    if system_type=="File":
        system = File.objects.filter(id=system_id)[0]
        book = rxncon_excel.ExcelBook(system.get_absolute_path())

    else:
        system = Quick.objects.filter(id=system_id)[0]
        book = rxncon_quick.Quick(system.quick_input)
    return book.rxncon_system

def create_rxncon_system_object(request, project_name, project_type, project_id):
    rxncon_system = create_rxncon_system(request, project_type, project_id)
    if rxncon_system:
        pickled_sys = pickle.dumps(rxncon_system)
        sys_obj = Rxncon_system(project_name=project_name, pickled_system = pickled_sys, project_id=project_id, project_type= project_type)
        sys_obj.save()
        print("Rxncon system for project '" + project_name + "' successfully created.")
        messages.info(request, "Rxncon system for project '" + project_name + "' successfully created.")
        return sys_obj


