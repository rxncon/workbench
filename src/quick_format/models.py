from django.core.urlresolvers import reverse
from django.db import models

class Quick(models.Model):
    name = models.CharField(max_length=120)
    quick_input = models.TextField(null=False)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)  # initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification,
    # updated gets reset when Post is updated -duh

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quick_format:quick_detail", kwargs={"id": self.id})

    def load(self):
        pass