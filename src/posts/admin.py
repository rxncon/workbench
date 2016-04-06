from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","updated", "timestamp"]
    list_display_links = ["__str__"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["__str__","content"]

    class Meta:
        model=Post

admin.site.register(Post, PostModelAdmin)