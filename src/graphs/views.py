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
from xml.dom import minidom



def regGraph(request, id=None):
    form = regGraphFileForm(request.POST or None)
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    if form.is_valid():
        if id:
            file = File.objects.get(id=id)
            try:
                book = rxncon_excel.ExcelBookWithReactionType(file.get_absolute_path())
            except:
                book = rxncon_excel.ExcelBookWithoutReactionType(file.get_absolute_path())
            rxncon_system = book.rxncon_system

            graph_file_name = file.slug + "_" + file.get_filename().split(".")[0] + "_regGraph.xgmml"
            graph_file_path = "%s/%s/%s/%s" % (media_root, file.slug, "graphs", graph_file_name)
            graph = regulatory_graph.RegulatoryGraph(rxncon_system).to_graph()
            xgmml_graph = graphML.XGMML(graph, file.slug)

            if os.path.exists(graph_file_path):
                messages.warning(request, "Graph File already exists.")
                return file_detail(request, id)
            if not os.path.exists("%s/%s/%s" % (media_root, file.slug, "graphs")):
                os.makedirs("%s/%s/%s" % (media_root, file.slug, "graphs"))

            graph_file = xgmml_graph.to_file(graph_file_path)
            graph_string = xgmml_graph.to_string()

            if request.FILES.get('template'):
                xmldoc_layouted = minidom.parse(request.FILES.get('template'))
                node_list_layouted = xmldoc_layouted.getElementsByTagName('node')
                node_names_layouted = [item._attrs['label'].value for item in node_list_layouted]

                xmldoc_raw = minidom.parse(graph_file_path)
                node_list_raw = xmldoc_raw.getElementsByTagName('node')
                node_names_raw = [{"name": item._attrs['label'].value,
                                   "index": _get_node_index(item._attrs['label'].value, node_list_raw)} for item in
                                  node_list_raw]

                coordinates_dict = _get_labels_and_coordinates_dict(xmldoc_layouted)
                print("node names raw: ", node_names_raw)
                print("node_names_layouted: ", node_names_layouted)
                for node in node_names_raw:
                    if node["name"] in node_names_layouted and node["name"] in coordinates_dict:
                        print ("node [\"name\"]: ", node["name"])
                        element = xmldoc_raw.createElement("graphics")
                        element.setAttribute("x", coordinates_dict[node["name"]]["x"])
                        element.setAttribute("y", coordinates_dict[node["name"]]["y"])
                        element.setAttribute("z", coordinates_dict[node["name"]]["z"])
                        element.appendChild(xmldoc_raw.createTextNode(''))
                        target_node = node_list_raw.item(node["index"])
                        target_node.appendChild(element)

                graph_file = open(graph_file_path, "w")
                xmldoc_raw.writexml(graph_file)
                graph_string = xmldoc_raw.toprettyxml()
                graph_file.close()

            g = Graph_from_File(project_name=file.project_name, graph_file=graph_file_path, graph_string=graph_string,
                                comment=request.POST.get('comment'))
            g.save()

            File.objects.filter(id=id).update(reg_graph=g)
            messages.info(request, "regulatory graph for project '" + g.project_name + "' successfully created.")
            return file_detail(request, id)

        else:

            return render(request, "regGraphFile_form.html")

    context = {
        "form": form,
    }
    return render(request, "regGraphFile_form.html", context)


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

def _get_labels_and_coordinates_dict(xmldoc):
    graphics_list = xmldoc.getElementsByTagName('graphics')

    coordinates_dict={}
    for graphic in graphics_list:
        if graphic._attrs and not graphic.parentNode.tagName=="edge":
            coordinates={
                "x": graphic._attrs['x'].value,
                "y": graphic._attrs['y'].value,
                "z": graphic._attrs['z'].value,
            }
            coordinates_dict[graphic.parentNode._attrs['label'].value] = coordinates

    return coordinates_dict

def _get_node_index(nodename, node_list):
    lenght = node_list.length
    for i in range(0,lenght):
        if nodename == node_list[i]._attrs['label'].value:
            return i