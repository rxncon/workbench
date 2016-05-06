from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import rxncon.input.excel_book.excel_book as rxncon_excel


from .models import Quick
from .forms import QuickForm, DeleteQuickForm


def quick_detail(request, id):
    instance = Quick.objects.filer(id=id)
    # book= rxncon_excel.ExcelBookWithReactionType(instance.get_absolute_path())
    # rxncon_system = book.rxncon_system

    context_data = {
        "title": instance.name,
        "instance":instance,
        # "book":book,
        # "nr_reactions":len(rxncon_system.reactions),
        "nr_reactions":"currently deactivated in fileTree/views.py",
    }
    return render(request, "quick_detail.html", context_data)


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
    name = q.name
    timestamp = q.timestamp
    if request.method == 'POST':
        form = DeleteQuickForm(request.POST, instance=q)

        if form.is_valid(): # checks CSRF
            q.delete()
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/") # wherever to go after deleting
    else:
        form = DeleteQuickForm(instance=q)
    template_vars = {'form': form,
                     'name': name,
                     "timestamp": timestamp,
                     }
    return render(request, 'quick_delete.html', template_vars)


