from django.views.generic import ListView

from .models import Moment


class MomentsFeedView(ListView):
    model = Moment
    context_object_name = 'moments'
    ordering = '-id'
    paginate_by = 2

    template_name = "moments_feed/moments_feed.html"
