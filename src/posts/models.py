from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os


def upload_location(instance, filename):
    #return "%s/%s" %(os.path.splitext(filename)[0],filename)
    return "%s/%s" %(instance.slug,filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return "/posts/%s/" %(self.id)
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
    slug = slugify(os.path.splitext(instance.image.name)[0])
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Post)