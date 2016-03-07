from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification, updated gets reset when Post is updated -duh

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return "/posts/%s/" %(self.id)
        return reverse("posts:detail", kwargs={"id":self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]