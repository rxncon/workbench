from django.shortcuts import render
from django.conf import settings
from .forms import regGraphFileForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from fileTree.models import File
from fileTree.views import file_detail
from .models import Graph_from_File
import os
import rxncon.input.excel_book.excel_book as rxncon_excel
import rxncon.simulation.rule_graph.regulatory_graph as regulatory_graph
import rxncon.simulation.rule_graph.graphML as graphML
from .forms import DeleteGraphForm



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
        graph_file_path =  "%s/%s/%s/%s" %(media_root,file.slug,"graphs",str(file.id)+".txt")
        if os.path.exists(graph_file_path):
            messages.warning(request, "Graph File already exists.")
            return file_detail(request, id)
        if not os.path.exists("%s/%s/%s" %(media_root,file.slug,"graphs")):
            os.makedirs("%s/%s/%s" %(media_root,file.slug,"graphs"))
        graph_file = xgmml_graph.to_file(graph_file_path)
        graph_string = xgmml_graph.to_string()
        g = Graph_from_File(project_name=file.project_name, graph_file=graph_file_path, graph_string=graph_string)
        g.save()
        File.objects.filter(id=id).update(reg_graph=g)
        messages.info(request, "regulatory graph for project '" + g.project_name + "' successfully created.")
        return file_detail(request, id)

    else:

        return render(request, "regGraphFile_form.html")

def graph_delete(request, pk):
    f = get_object_or_404(Graph_from_File, pk=pk)
    project_name = f.project_name
    timestamp = f.timestamp
    filename = f.get_filename()
    file_id = File.objects.get(reg_graph=f).id
    slug = f.slug
    if request.method == 'POST':
        form = DeleteGraphForm(request.POST, instance=f)

        if form.is_valid(): # checks CSRF
            f.delete()
            os.remove(f.graph_file.name)
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/files/"+str(file_id)+"/") # wherever to go after deleting
    else:
        form = DeleteGraphForm(instance=f)
    template_vars = {'form': form,
                     'project_name': project_name,
                     "timestamp": timestamp,
                     "file": filename,
                     }
    return render(request, 'graph_delete.html', template_vars)