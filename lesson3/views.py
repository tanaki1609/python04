from rest_framework import serializers, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from lesson3.models import News, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = 'id title description comments'.split()


class NewsCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)


class NewsApiView(APIView):
    allowed_methods = ['get', 'post']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        articles = News.objects.filter(author=request.user)
        return Response(data=self.serializer_class(articles,
                                                   many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            article = News.objects.create(title=serializer.title,
                                          description=serializer.description)
            article.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class NewsDetailView(APIView):
    allowed_methods = ['get', 'post']

    def get(self, request, id):
        articles = News.objects.get(id=id)
        return Response(data=NewsSerializer(articles, many=False).data)

    def post(self, request, id):
        news = News.objects.get(id=id)
        comment = request.data.get('comment')
        new_comment = Comment.objects.create(text=comment, news=news)
        new_comment.save()
        return Response(status=status.HTTP_201_CREATED)


class NewsViewSet(mixins.ListModelMixin,GenericViewSet):
    def list(self, request, *args, **kwargs):
        articles = News.objects.all()
        return Response(data=self.serializer_class(articles,
                                                   many=True).data)
