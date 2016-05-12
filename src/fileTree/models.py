from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render_to_response
from django.utils.text import slugify



def upload_location(instance, filename):
    #return "%s/%s" %(os.path.splitext(filename)[0],filename)
    return "%s/%s" %(instance.slug,filename)

class File(models.Model):
    project_name = models.CharField(max_length=120)
    loaded = models.BooleanField(default=False)
    older_version_ids=[]
    slug = models.SlugField(blank=True) # TODO: take blank out when file_upload with automated slug creation is done
    file = models.FileField(upload_to=upload_location, null=False, blank=False)
    comment= models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh

    def __str__(self):
        return self.file.name
    def __unicode__(self):
        return self.file.name

    def get_filename(self):
        return str(self.file.name).split("/")[-1]

    def get_project_slug(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("fileTree:detail", kwargs={"id": self.id})

    def upload_new_version(self):
        return reverse("fileTree:upload", kwargs={"slug": self.slug, })

    def get_download_url(self):
        media_url= settings.MEDIA_URL
        return media_url+"%s" %(self.file)

    def get_absolute_path(self):
        media_root=settings.MEDIA_ROOT
        return media_root+"/%s" %(self.file)


    class Meta:
        ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
    slug = slugify(instance.project_name)
    # if new_slug is not None:
    #     slug = new_slug
    # qs = File.objects.filter(slug=slug).order_by("-id")
    # exists = qs.exists()
    # if exists:
    #     new_slug = "%s-%s" %(slug, qs.first().id)
    #     return create_slug(instance, new_slug=new_slug)
    # return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug=slugify(instance.project_name)



pre_save.connect(pre_save_post_receiver, sender=File)