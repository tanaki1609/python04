from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson3.models import News
from lesson3.views import NewsSerializer


class NewsApiView(APIView, PageNumberPagination):
    allowed_methods = ['get']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        news = News.objects.filter(Q(title__contains=query) |
                                   Q(description__contains=query))
        results = self.paginate_queryset(news, request, view=self)
        return self.get_paginated_response(self.serializer_class(results,
                                                                 many=True).data)


PAGE_SIZE = 3


class NewsCustomApiView(APIView):
    allowed_methods = ['get']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get('page', '1'))
        news = News.objects.all()[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]  # [0:3]
        return Response(data=self.serializer_class(news, many=True).data)
