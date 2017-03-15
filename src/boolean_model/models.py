from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


def upload_location(instance, filename):
    #return "%s/%s" %(os.path.splitext(filename)[0],filename)
    return "%s/%s/%s" %(instance.slug,"graphs",filename)

class Bool_from_rxnconsys(models.Model):
    project_name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True) # TODO: take blank out when file_upload with automated slug creation is done
    comment= models.TextField(null=True, blank=True)
    smoothing = models.ChoiceField(choices=["no_smoothing", "smooth_production_sources"], default="no_smoothing", help_text="Smoothing strategy.")


    boolnet_file_path = models.FileField(null=True)
    graph_string = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh

    def __str__(self):
        return self.project_name

    def __unicode__(self):
        return self.project_name

    def get_filename(self):
        return str(self.graph_file.name).split("/")[-1]

    def get_project_slug(self):
        return self.slug

    def upload_new_version(self):
        return reverse("fileTree:upload", kwargs={"slug": self.slug, })

    def get_relative_path(self):
        return str(self.graph_file).split("/media_cdn/")[-1]

    def get_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.get_relative_path())

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
