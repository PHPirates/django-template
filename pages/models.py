from django.db import models
from django.utils import timezone


class Article(models.Model):
    """" This model is an article. """
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self) -> None:
        """" Publish article now. """
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        """ Python to-string method. """
        return self.title
