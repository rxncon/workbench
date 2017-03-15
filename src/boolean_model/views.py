from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from fileTree.models import File
from fileTree.views import file_detail
from .forms import boolForm
from .forms import DeleteBoolForm
from .models import Bool_from_rxnconsys
import os
from quick_format.models import Quick
from quick_format.views import quick_detail
import rxncon.input.excel_book.excel_book as rxncon_excel
import rxncon.input.quick.quick as rxncon_quick
import rxncon.simulation.boolean.boolean_model as rxncon_boolean_model
import rxncon.simulation.boolean.boolnet_from_boolean_model as bfbm
import global_scripts.rxncon2boolnet as r2b


def create_rxncon_system(system, system_type):
    if system_type == "File":
        try:
            book = rxncon_excel.ExcelBook(system.get_absolute_path())
        except:
            book = rxncon_excel.ExcelBook(system.get_absolute_path())
    else:
        book = rxncon_quick.Quick(system.quick_input)
    return book.rxncon_system


def check_filepath(request, graph_file_path, file, media_root):
    if os.path.exists(graph_file_path):
        messages.warning(request, "Boolean model files already exist. Delete first in the system's detail view.")
        return False
    elif not os.path.exists("%s/%s/%s" % (media_root, file.slug, "graphs")):
        os.makedirs("%s/%s/%s" % (media_root, file.slug, "graphs"))
        return True
    else:
        return True

def bool(request, system_id=None):
    form = boolForm(request.POST or None)

    if not form.is_valid() and not system_id:
        context = {
            "form": form,
        }
        return render(request, "bool_form.html", context)


  # --smoothing TEXT       Smoothing strategy. Default: no_smoothing. Choices:
  #                        no_smoothing, smooth_production_sources
  # --knockout TEXT        Generate knockouts. Default: no_knockout. Choices:
  #                        no_knockout, knockout_neutral_states,
  #                        knockout_all_states
  # --overexpression TEXT  Generate overexpressions. Default: no_overexpression.
  #                        Choices: no_overexpression,
  #                        overexpress_neutral_states, overexpress_all_states
  # --k_plus TEXT          Strategy for handling k+ contingencies. Default:
  #                        strict. Choices: strict, ignore
  # --k_minus TEXT         Strategy for handling k- contingencies. Default:
  #                        strict. Choices: strict, ignore


class Bool(View):
    def post(self, request, system_id=None):
        self.system_id = system_id
        self.request = request
        self.form = boolForm(self.request.POST or None)

        if self.form.is_valid():
            media_url = settings.MEDIA_URL
            media_root = settings.MEDIA_ROOT
            system_type = None
            try:
                system = Quick.objects.filter(id=system_id)[0]
                system_type = "Quick"
                project_name = system.name
            except:
                system = File.objects.filter(id=system_id)[0]
                system_type = "File"
                project_name = system.project_name

            boolnet_model_filename = system.slug + "_model.boolnet"
            boolnet_symbol_filename = system.slug + "_symbols.csv"
            boolnet_initial_val_filename = system.slug + "_initial_vals.csv"

            model_path = "%s/%s/%s/%s" % (media_root, system.slug, "boolnet", boolnet_model_filename)
            symbol_path = "%s/%s/%s/%s" % (media_root, system.slug, "boolnet", boolnet_symbol_filename)
            init_path = "%s/%s/%s/%s" % (media_root, system.slug, "boolnet", boolnet_initial_val_filename)

            for path in [model_path, symbol_path, init_path]:
                if not check_filepath(request, path, system, media_root):
                    if system_type == "Quick":
                        return quick_detail(request, system_id)
                    else:
                        return file_detail(request, system_id)

            rxncon_system = create_rxncon_system(system, system_type)

            smoothing = request.POST.get('smoothing') #TODO: geht das?
            print("smoothing strategy from post: " + smoothing)

            model_str, symbol_str, initial_val_str = r2b.boolnet_strs_from_rxncon(rxncon_system, smoothing_strategy = smoothing)
            # model_str, symbol_str, initial_val_str = boolnet_strs_from_rxncon(rxncon_system,
            #                                                                   smoothing_strategy=smoothing,
            #                                                                   knockout_strategy,
            #                                                                   overexpression_strategy, k_plus_strategy,
            #                                                                   k_minus_strategy)
            with open(model_path, mode='w') as f:
                f.write(model_str)

            with open(symbol_path, mode='w') as f:
                f.write(symbol_str)

            with open(init_path, mode='w') as f:
                f.write(initial_val_str)

            b = Bool_from_rxnconsys(project_name=project_name, model_path=model_path, symbol_path=symbol_path, init_path=init_path,
                                comment=request.POST.get('comment'))
            b.save()
            messages.info(request, "boolnet files for project '" + g.project_name + "' successfully created.")
            if system_type == "Quick":
                Quick.objects.filter(id=system_id).update(boolean_model=b)
                return quick_detail(request, system_id)
            else:
                File.objects.filter(id=system_id).update(boolean_model=b)
                return file_detail(request, system_id)




def graph_delete(request, pk):
    f = get_object_or_404(Graph_from_File, pk=pk)
    project_name = f.project_name
    timestamp = f.timestamp
    filename = f.get_filename()
    system_type = None
    try:
        if File.objects.filter(reg_graph=f):
            id = File.objects.filter(reg_graph=f)[0].id
        else:
            id = File.objects.filter(rea_graph=f)[0].id

    except:
        if Quick.objects.filter(reg_graph=f):
            id = Quick.objects.filter(reg_graph=f)[0].id
        else:
            id = Quick.objects.filter(rea_graph=f)[0].id
        system_type = "Quick"

    slug = f.slug
    if request.method == 'POST':
        form = DeleteGraphForm(request.POST, instance=f)

        if form.is_valid(): # checks CSRF
            f.delete()
            os.remove(f.graph_file.name)
            messages.success(request, "Successfully deleted")
            if system_type == "Quick":
                return HttpResponseRedirect("/quick/"+str(id)+"/") # wherever to go after deleting

            else:
                return HttpResponseRedirect("/files/" + str(id) + "/")  # wherever to go after deleting
    else:
        form = DeleteGraphForm(instance=f)
    template_vars = {'form': form,
                     'project_name': project_name,
                     "timestamp": timestamp,
                     "file": filename,
                     }
    return render(request, 'graph_delete.html', template_vars)



