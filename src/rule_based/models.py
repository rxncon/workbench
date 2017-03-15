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
    slug = models.SlugField(blank=True)
    comment= models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)  # initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True,
                                   auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh
    # rxncon2bngl
    model_path = models.FileField(null=True)
    symbol_path = models.FileField(null=True)
    init_path = models.FileField(null=True)

    def __str__(self):
        return self.project_name

    def __unicode__(self):
        return self.project_name

    def get_model_filename(self):
        return str(self.model_path.name).split("/")[-1]
    def get_symbol_filename(self):
        return str(self.symbol_path.name).split("/")[-1]
    def get_init_filename(self):
        return str(self.init_path.name).split("/")[-1]

    def get_project_slug(self):
        return self.slug

    def get_relative_model_path(self):
        return str(self.model_path).split("/media_cdn/")[-1]
    def get_relative_symbol_path(self):
        return str(self.symbol_path).split("/media_cdn/")[-1]
    def get_relative_init_path(self):
        return str(self.init_path).split("/media_cdn/")[-1]

    def get_model_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.get_relative_model_path())
    def get_symbol_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.get_relative_symbol_path())
    def get_init_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.get_relative_init_path())

    class Meta:
        ordering = ["-updated", "-timestamp"]

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug = slugify(instance.project_name)

pre_save.connect(pre_save_post_receiver, sender=Bool_from_rxnconsys)
