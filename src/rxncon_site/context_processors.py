from fileTree.models import File
from quick_format.models import Quick
from django.conf import settings
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
        "projects_length": len(projects),
        # "page_request_var":page_request_var,
    }

def quick_list(request):
    quick_definitions= Quick.objects.all().order_by("-updated")  # all quicks
    return {
        "quick_definitions": quick_definitions,
        "quick_definitions_length": len(quick_definitions),
        "title"      : "Quick definitions",
    }

def get_loaded_system(request):
    context ={} #initialise output

    loaded_system_list = File.objects.filter(loaded=True)
    if len(loaded_system_list) == 0: # must be quick format
        loaded_system_list = Quick.objects.filter(loaded=True)

        if len(loaded_system_list) == 1:
            system_type = "Quick"
            instance = loaded_system_list[0]
            name = instance.name
            slug= instance.slug
            filename="" # there is no corresponding file

    else: #must be file format
        system_type = "File"
        instance = loaded_system_list[0]
        name = instance.project_name
        filename = instance.get_filename()
        slug = instance.slug

    if len(loaded_system_list) > 1:
        raise LookupError("Corrupted database, multiple systems had loaded flag set to true.")

    if len(loaded_system_list) != 0:

        context = {
            "loaded_system": instance,
            "loaded_type": system_type,
            "loaded_project_name": name,
            "loaded_project_slug": slug,
        }
        if filename:
            context["loaded_file"] = filename
    return context

def admin_media(request):

    return {'MEDIA_ROOT': settings.MEDIA_ROOT}
