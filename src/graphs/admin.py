from django.contrib import admin
from .models import Graph_from_File

class GraphFromFileModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","connected_system","updated", "timestamp"]
    list_display_links = ["__str__"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["__str__","content"]

    class Meta:
        model=Graph_from_File

admin.site.register(Graph_from_File, GraphFromFileModelAdmin)
