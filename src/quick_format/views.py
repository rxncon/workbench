from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import rxncon.input.quick.quick as rxncon_quick
import rxncon.input.excel_book.excel_book as rxncon_excel



from .models import Quick
from fileTree.models import File
from .forms import QuickForm, DeleteQuickForm


def quick_detail(request, id, compare_dict=None):
    instance = Quick.objects.get(id=id)
    rxncon_system = rxncon_quick.Quick(instance.quick_input)

    context_data = {
        "title": instance.name,
        "instance": instance,
        "nr_reactions": len(rxncon_system.rxncon_system.reactions),
        "nr_contingencies": len(rxncon_system.rxncon_system.contingencies),
        "loaded": instance.loaded,
    }

    if compare_dict:
        context_data.update(compare_dict)

    return render(request, "quick_detail.html", context_data)


def quick_compare(request, id):
    loaded = File.objects.filter(loaded=True)
    if loaded:
        try:
            loaded_rxncon = rxncon_excel.ExcelBook(loaded[0].get_absolute_path())
        except:
            raise ImportError("Could not import file")

    else:
        loaded = Quick.objects.get(loaded=True)
        try:
            loaded_rxncon = rxncon_quick.Quick(loaded.quick_input)
        except:
            raise ImportError("Could not import quick")


    loaded_rxncon_system = loaded_rxncon.rxncon_system

    compare_dict = {
        "compare_nr_reactions": len(loaded_rxncon_system.reactions),
        "compare_nr_contingencies": len(loaded_rxncon_system.contingencies),
    }


    return quick_detail(request, id, compare_dict)


def quick_new(request):
    # TODO: like this, it is not case sensitive. "Elefant" and "elefant" are the same project
    form = QuickForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context={
        "form": form,
    }
    return render(request, "quick_form.html", context)


def quick_delete(request, id):
    q = get_object_or_404(Quick, id=id)
    if request.method == 'POST':
        form = DeleteQuickForm(request.POST, instance=q)

        if form.is_valid(): # checks CSRF
            q.delete()
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/") # wherever to go after deleting
    else:
        form = DeleteQuickForm(instance=q)
    template_vars = {'form': form,
                     'name': q.name,
                     'timestamp': q.timestamp,
                     'quick_input': q.quick_input,
                     }
    return render(request, 'quick_delete.html', template_vars)

def quick_update(request, id=None):
    instance = get_object_or_404(Quick, id=id)
    form = QuickForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        "title": instance.name,
        "instance":instance,
        "form": form,
    }
    return render(request, "quick_form.html", context_data)

def quick_load(request, id):
    File.objects.all().update(loaded=False)
    Quick.objects.all().update(loaded=False)
    target = Quick.objects.filter(id=id)
    target.update(loaded=True)
    if target[0].loaded:
        messages.info(request, "Quick definition '" + target[0].name + "' successfully loaded")
    return quick_detail(request, id)


