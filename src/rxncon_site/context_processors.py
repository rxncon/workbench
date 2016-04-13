from fileTree.models import File

# http://stackoverflow.com/questions/28533854/provide-extra-context-to-all-views

def file_list(request):
    # queryset_list = File.objects.all()
    queryset_list = File.objects.all().order_by("-updated") # all files

    slug_list = []  # unique slugs in correct order
    for file in queryset_list:
        # get unique slug list in correct order
        current_slug= file.get_project_slug()
        if not current_slug in slug_list:
            slug_list.append(current_slug)

    projects= [queryset_list.filter(slug=slug).order_by("-updated") for slug in slug_list] # list of lists of files



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
