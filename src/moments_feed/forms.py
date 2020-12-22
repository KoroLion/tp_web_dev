from django.utils import timezone
from django.forms import ModelForm, CharField
from django.utils.html import strip_tags

from moments_feed.models import Moment, Tag


class MomentCreateForm(ModelForm):
    tags = CharField(max_length=255, label='Tags', help_text='Divide tags with coma and space')

    class Meta:
        model = Moment
        fields = ('description', 'image')

    @staticmethod
    def __add_tags(moment, tags):
        tags = tags.replace(' ', '').split(',')
        for name in tags:
            name = strip_tags(name)
            tag = Tag.objects.filter(name=name)
            if len(tag) != 0:
                tag = tag[0]
                tag.moment.add(moment)
            else:
                tag = Tag(name=name)
                tag.save()
                tag.moment.add(moment)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = user
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=False):
        super().save(commit)
        self.instance.author = self.author
        self.instance.created_date = timezone.now()
        self.instance.save()
        self.__add_tags(self.instance, self.cleaned_data['tags'])
        return self.instance
