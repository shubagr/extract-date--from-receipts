from django.db import models


class image(models.Model):
    image_string= models.TextField()


    def __str__(self):
        return "image %s" % self.image_string