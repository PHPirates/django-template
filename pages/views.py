""" This file contains the views, the 'pages' of the website. """
from django.utils import timezone
from django.views import generic

from .models import Article


# class IndexView(generic.TemplateView):
class IndexView(generic.ListView):
    """" Index of all pages, i.e. home page. """
    template_name = 'pages/index.html'
    # Provide name of the context variable returned by get_queryset?
    context_object_name = 'article_list'

    def get_queryset(self) -> None:
        """" Find the home article and display it. """
        return Article.objects.filter(published_date__lt=timezone.now()).order_by('published_date')

# Without a class:
# def index(request):
#     return render(request, 'pages/index.html', context={})
