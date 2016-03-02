from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# function based view, easier than class based but less strong
from .models import Post
from .forms import PostForm

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context_data = {
        "title": instance.title,
        "instance":instance,
    }
    return render(request, "post_detail.html", context_data)

def post_list(request):
    queryset = Post.objects.all().order_by('-updated')
    if request.user.is_authenticated():
        context_data = {
            "object_list":queryset,
            "title":"List"
        }

    return render(request, "post_list.html", context_data)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        "title": instance.title,
        "instance":instance,
        "form": form,
    }
    return render(request, "post_form.html", context_data)

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")

    return redirect("post:list")

