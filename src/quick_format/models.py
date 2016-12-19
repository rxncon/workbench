from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
# from graphs.models import Graph_from_Quick


class Quick(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    loaded = models.BooleanField(default=False)
    quick_input = models.TextField(null=False)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)  # initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification,
    # updated gets reset when Post is updated -duh
    # reg_graph = models.ForeignKey(Graph_from_Quick, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quick_format:quick_detail", kwargs={"id": self.id})

    def load(self):
        pass

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug=slugify(instance.name)



pre_save.connect(pre_save_post_receiver, sender=Quick)