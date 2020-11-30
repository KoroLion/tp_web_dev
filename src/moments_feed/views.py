import json

from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http.response import HttpResponse

from .models import Moment, Comment, Tag, Like


class MomentsListView(ListView):
    model = Moment
    context_object_name = 'moments'
    ordering = '-id'
    paginate_by = 2
    template_name = 'moments_feed/moments_best.html'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            tag = get_object_or_404(Tag, name=search)
            return tag.moment.all()

        return super().get_queryset()


class MomentsFeedView(MomentsListView):
    template_name = 'moments_feed/moments_feed.html'


class MomentView(DetailView):
    model = Moment
    context_object_name = 'moment'
    template_name = 'moments_feed/moment.html'

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content', None)
        like_moment = request.POST.get('like_moment', None)
        if content:
            c = Comment(author=request.user, moment=self.get_object(), content=content, created_date=timezone.now())
            c.save()
            return redirect(reverse('moment', args=(kwargs.get('pk', None),)))
        elif like_moment:
            moment = self.get_object()
            likes = Like.objects.filter(moment=moment, author=request.user)
            if len(likes) == 0:
                like = Like(moment=moment, author=request.user, created_date=timezone.now())
                like.save()
            else:
                Like.objects.filter(moment=moment, author=request.user).delete()

            return HttpResponse(json.dumps({
                'likesAmount': moment.like_set.count()
            }))
