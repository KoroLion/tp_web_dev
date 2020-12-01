from user_profile.models import User
from moments_feed.models import Moment, Like
from rest_framework import routers, serializers, viewsets, pagination
from django.db.models import Count


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='moments_best')

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.annotate(num_moments=Count('moment')).order_by('-num_moments')
    serializer_class = UserSerializer

    pagination_class = StandardResultsSetPagination


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    moment = serializers.PrimaryKeyRelatedField(queryset=Moment.objects.all())

    class Meta:
        model = Like
        fields = ['moment', 'author', 'created_date']


class LikeSetView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    pagination_class = StandardResultsSetPagination


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = ['author', 'description', 'image', 'created_date']


class MomentViewSet(viewsets.ModelViewSet):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer
    pagination_class = StandardResultsSetPagination


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'moments', MomentViewSet)
router.register(r'likes', LikeSetView)
