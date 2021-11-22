from django.contrib import admin

from moments_feed.models import Moment, Comment, Subscription, Tag


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('author', 'description', 'created_date')


@admin.register(Comment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('content', 'moment', 'author', 'created_date')


admin.site.register(Subscription)
admin.site.register(Tag)
