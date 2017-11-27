""" Models are objects used in the website. """
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


class Article(models.Model):
    """" This model is an article. """
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    # An HTMLField will use the TinyMCE editor, a TextField won't
    text = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self) -> None:
        """" Publish article now. """
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        """ Python to-string method. """
        return self.title
