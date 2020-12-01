import json

from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http.response import HttpResponse

from moments_feed.models import Moment, Comment, Tag, Like
from moments_feed.forms import MomentCreateForm


class MomentsListView(ListView):
    model = Moment
    context_object_name = 'moments'
    ordering = '-id'
    paginate_by = 4 * 3  # 3 per row
    template_name = 'moments_feed/moments_best.html'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            tag = Tag.objects.filter(name=search)
            if len(tag) != 0:
                return tag[0].moment.all()
            else:
                # nothing found = empty list
                return list()

        return super().get_queryset()


class MomentsFeedView(MomentsListView):
    paginate_by = 10
    template_name = 'moments_feed/moments_feed.html'


class MomentAddView(CreateView):
    model = Moment
    template_name = 'moments_feed/moment_add.html'
    form_class = MomentCreateForm

    def get_success_url(self):
        print(self.object)
        return reverse('moment', args=(self.object.pk,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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
