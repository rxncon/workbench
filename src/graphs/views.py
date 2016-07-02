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



def regGraph(request, file_id=None):
    form = regGraphFileForm(request.POST or None)

    if not form.is_valid() and not file_id:
        context = {
            "form": form,
        }
        return render(request, "regGraphFile_form.html", context)

    else:
        media_url = settings.MEDIA_URL
        media_root = settings.MEDIA_ROOT
        file = File.objects.get(id=file_id)
        graph_file_name = file.slug + "_" + file.get_filename().split(".")[0] + "_regGraph.xgmml"
        graph_file_path = "%s/%s/%s/%s" % (media_root, file.slug, "graphs", graph_file_name)
        if not check_filepath(request, graph_file_path, file, media_root):
            return file_detail(request, file_id)
        rxncon_system = create_rxncon_system(file)
        graph_file, graph_string = create_graph_without_template(request, media_root, file, rxncon_system, graph_file_path)

        if request.FILES.get('template'):
            graph_file, graph_string = apply_template_layout(request, graph_file_path)

        g = Graph_from_File(project_name=file.project_name, graph_file=graph_file_path, graph_string=graph_string,
                            comment=request.POST.get('comment'))
        g.save()

        File.objects.filter(id=file_id).update(reg_graph=g)
        messages.info(request, "regulatory graph for project '" + g.project_name + "' successfully created.")
        return file_detail(request, file_id)


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

def create_rxncon_system(file):
    try:
        book = rxncon_excel.ExcelBookWithReactionType(file.get_absolute_path())
    except:
        book = rxncon_excel.ExcelBookWithoutReactionType(file.get_absolute_path())
    return book.rxncon_system


def create_graph_without_template(request, media_root, file, rxncon_system, graph_file_path):
    graph = regulatory_graph.RegulatoryGraph(rxncon_system).to_graph()
    xgmml_graph = graphML.XGMML(graph, file.slug)
    graph_file = xgmml_graph.to_file(graph_file_path)
    graph_string = xgmml_graph.to_string()

    return graph_file, graph_string

def check_filepath(request, graph_file_path, file, media_root):
    if os.path.exists(graph_file_path):
        messages.warning(request, "Graph File already exists.")
        return False
    elif not os.path.exists("%s/%s/%s" % (media_root, file.slug, "graphs")):
        os.makedirs("%s/%s/%s" % (media_root, file.slug, "graphs"))
    else:
        return True

def apply_template_layout(request, graph_file_path):
    template_file = request.FILES.get('template')
    graph_data_unlayouted = get_graph_nodes_and_lables_from_file(graph_file_path)
    graph_data_layouted = get_graph_nodes_and_lables_from_file(template_file)
    node_names_layouted = [d["name"] for d in graph_data_layouted["node_names_dicts"]]
    graph_data_now_layouted = insert_graphics_elements_into_graph(graph_data_unlayouted, graph_data_layouted, node_names_layouted)
    graph_file = open(graph_file_path, "w")
    graph_data_now_layouted["xmldoc"].writexml(graph_file)
    graph_string = graph_data_now_layouted["xmldoc"].toprettyxml()
    graph_file.close()

    return graph_file, graph_string

def insert_graphics_elements_into_graph(graph_data_unlayouted, graph_data_layouted, node_names_layouted):
    coordinates_dict = _get_labels_and_coordinates_dict(graph_data_layouted["xmldoc"])
    for item in graph_data_unlayouted["node_names_dicts"]:
        if item["name"] in node_names_layouted and item["name"] in coordinates_dict:
            element = graph_data_unlayouted["xmldoc"].createElement("graphics")
            element.setAttribute("x", coordinates_dict[item["name"]]["x"])
            element.setAttribute("y", coordinates_dict[item["name"]]["y"])
            element.setAttribute("z", coordinates_dict[item["name"]]["z"])
            element.appendChild(graph_data_unlayouted["xmldoc"].createTextNode(''))
            target_node = graph_data_unlayouted["node_list"].item(item["index"])
            target_node.appendChild(element)
    return graph_data_unlayouted

def get_graph_nodes_and_lables_from_file(file):
    xmldoc = minidom.parse(file)
    node_list = xmldoc.getElementsByTagName('node')
    node_names_dicts = [{"name": item._attrs['label'].value,
                        "index": _get_node_index(item._attrs['label'].value, node_list)} for item in
                       node_list]

    return {"xmldoc": xmldoc, "node_list": node_list, "node_names_dicts": node_names_dicts}

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
