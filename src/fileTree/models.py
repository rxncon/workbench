from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render_to_response
from django.utils.text import slugify
from graphs.models import Graph_from_File
from boolean_model.models import Bool_from_rxnconsys
from rule_based.models import Rule_based_from_rxnconsys
from rxncon_system.models import Rxncon_system
import os
import shutil
import rxncon.input.excel_book.excel_book as rxncon_excel
from django.contrib import messages


#TODO: PEP-8 coding style
def upload_location(instance, filename):
    return "%s/%s" %(instance.slug,filename)


class File(models.Model):
    project_name = models.CharField(max_length=120)
    loaded = models.BooleanField(default=False)
    slug = models.SlugField(blank=True) # TODO: take blank out when file_upload with automated slug creation is done
    file = models.FileField(upload_to=upload_location, null=False, blank=False)
    comment= models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh
    rxncon_system = models.ForeignKey(Rxncon_system, null=True, on_delete=models.SET_NULL, blank=True, related_name="rxncon_system_file") #pickled object
    reg_graph = models.ForeignKey(Graph_from_File, null=True, on_delete=models.SET_NULL, blank=True, related_name="regulatory_graph_file")
    rea_graph = models.ForeignKey(Graph_from_File, null=True, on_delete=models.SET_NULL, blank=True, related_name="reaction_graph_file")
    sRea_graph = models.ForeignKey(Graph_from_File, null=True, on_delete=models.SET_NULL, blank=True, related_name="species reaction_graph_file+")
    boolean_model = models.ForeignKey(Bool_from_rxnconsys, null=True, on_delete=models.SET_NULL, blank=True, related_name="bool_file")
    rule_based_model = models.ForeignKey(Rule_based_from_rxnconsys, null=True, on_delete=models.SET_NULL, blank=True, related_name="rule_based_file")

    def __str__(self):
        return self.file.name

    def __unicode__(self):
        return self.file.name

    def load(self):
        return reverse("fileTree:load", kwargs={"id": self.id})

    def get_filename(self):
        return str(self.file.name).split("/")[-1]

    def get_project_slug(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("fileTree:detail", kwargs={"id": self.id})

    def upload_new_version(self):
        return reverse("fileTree:upload", kwargs={"slug": self.slug, })

    # def get_pickled_rxncon_system(self):
    #     return self.rxncon_system.get_pickled_system()

    def get_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.file)

    def get_absolute_path(self):
        media_root = settings.MEDIA_ROOT
        return media_root+"/%s" %(self.file)

    def delete_file_from_harddisk(self):
        path = self.get_absolute_path()
        os.remove(path)

    def delete_project_from_harddisk(self):
        path = self.get_absolute_path()
        path = os.path.dirname(path)
        shutil.rmtree(path)

    # def create_rxncon_system(self):
    #     try:
    #         book= rxncon_excel.ExcelBook(self.get_absolute_path())
    #         self.rxncon_system = book.rxncon_system
    #         self.save(force_update=True)
    #         print(self.rxncon_system.reactions)
    #         print("Created rxncon_system.")
    #     except ImportError as error:
    #         messages.add_message(messages.ERROR, error)


    class Meta:
        ordering = ["-updated", "-timestamp"]



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.project_name)



pre_save.connect(pre_save_post_receiver, sender=File)