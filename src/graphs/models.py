from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render_to_response
from django.utils.text import slugify
from fileTree.models import File
from quick_format.models import Quick


def upload_location(instance, filename):
    #return "%s/%s" %(os.path.splitext(filename)[0],filename)
    return "%s/%s/%s" %(instance.slug,"graphs",filename)

class Graph_from_File(models.Model):
    connected_system = models.ForeignKey(File, on_delete=models.CASCADE, null=True)
    project_name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True) # TODO: take blank out when file_upload with automated slug creation is done
    comment= models.TextField(null=True, blank=True)
    graph_file = models.FileField(null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh

    def __str__(self):
        return self.project_name

    def __unicode__(self):
        return self.project_name

    def get_filename(self):
        return str(self.file.name).split("/")[-1]

    def get_project_slug(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("fileTree:detail", kwargs={"id": self.connected_system.id})

    def upload_new_version(self):
        return reverse("fileTree:upload", kwargs={"slug": self.slug, })

    def get_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.file)

    def get_absolute_path(self):
        media_root=settings.MEDIA_ROOT
        return media_root+"/%s" %(self.file)


    class Meta:
        ordering = ["-updated", "-timestamp"]

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug = slugify(instance.project_name)

pre_save.connect(pre_save_post_receiver, sender=Graph_from_File)