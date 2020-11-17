from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import redirect, reverse

from .models import Moment, Comment


class MomentsListView(ListView):
    model = Moment
    context_object_name = 'moments'
    ordering = '-id'
    paginate_by = 2
    template_name = 'moments_feed/moments_best.html'


class MomentsFeedView(MomentsListView):
    template_name = 'moments_feed/moments_feed.html'


class MomentView(DetailView):
    model = Moment
    context_object_name = 'moment'
    template_name = 'moments_feed/moment.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            content = request.POST.get('content', None)
            if content:
                c = Comment(author=request.user, moment=self.get_object(), content=content, created_date=timezone.now())
                c.save()

        return redirect(reverse('moment', args=(kwargs.get('pk', None),)))
