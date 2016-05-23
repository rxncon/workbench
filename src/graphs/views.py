from django.shortcuts import render
from .forms import regGraphFileForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import rxncon.input.excel_book.excel_book as rxncon_excel
import rxncon.simulation.rule_graph.regulatory_graph as regulatory_graph
import rxncon.simulation.rule_graph.graphML as graphML


def regGraph(request):
    form = regGraphFileForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "regGraphFile_form.html", context)
