from fileTree.models import File


# http://stackoverflow.com/questions/28533854/provide-extra-context-to-all-views

def file_list(request):
    # queryset_list = File.objects.all()
    queryset_list = File.objects.all().order_by("slug", "-updated")
    slug_list = list(set([File.get_project_slug() for File in queryset_list])) # list(set()) to get unique values
    projects= [queryset_list.filter(slug=slug).order_by("-updated") for slug in slug_list]



    # paginator = Paginator(queryset_list, 10)
    # page_request_var= "page"
    # page = request.GET.get('page_request_var')
    # try:
    #     queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     queryset = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     queryset = paginator.page(paginator.num_pages)

    return {
        # "object_list":queryset,
        "object_list":queryset_list,
        "title":"Projects",
        "slug_list": slug_list,
        "projects": projects,
        # "page_request_var":page_request_var,
    }
