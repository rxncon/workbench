from django.shortcuts import render
from django.conf import settings
from .forms import regGraphFileForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import os
import rxncon.input.excel_book.excel_book as rxncon_excel
import rxncon.simulation.rule_graph.regulatory_graph as regulatory_graph
import rxncon.simulation.rule_graph.graphML as graphML
from .models import Graph_from_File
from fileTree.models import File
from fileTree.views import file_detail


def regGraph(request, id=None):
    # form = regGraphFileForm(request.POST or None)
    #
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.save()
    #     messages.success(request, "Successfully created")
    #     return HttpResponseRedirect(instance.get_absolute_url())
    #
    # context = {
    #     "form": form,
    # }
    # return render(request, "regGraphFile_form.html", context)
    if id:
        media_url = settings.MEDIA_URL
        media_root= settings.MEDIA_ROOT
        file = File.objects.get(id=id)
        try:
            book = rxncon_excel.ExcelBookWithReactionType(file.get_absolute_path())
        except:
            book = rxncon_excel.ExcelBookWithoutReactionType(file.get_absolute_path())
        rxncon_system = book.rxncon_system
        graph = regulatory_graph.RegulatoryGraph(rxncon_system).to_graph() # throws not implemented errorim
        xgmml_graph = graphML.XGMML(graph, file.slug)
        if not os.path.exists("%s%s/%s" %(media_url,file.slug,"graphs")):
            os.makedirs("%s%s/%s" %(media_url,file.slug,"graphs"))
        graph_file_path_relative =  "%s%s/%s/%s" %(media_url,file.slug,"graphs",str(file.id)+".txt")
        graph_file = xgmml_graph.to_file(graph_file_path_relative)
        graph_string = xgmml_graph.to_string()
        g = Graph_from_File(connected_system=file, project_name=file.project_name, graph_file=graph_file_path_relative)
        g.save()
        messages.info(request, "regulatory graph for project '" + g.project_name + "' successfully created.")
        return file_detail(request, id)

    else:

        return render(request, "regGraphFile_form.html")
