"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from lesson1 import views
from lesson2 import views as article_views
from lesson3 import views as news_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/courses/', views.get_all_courses),
    path(r'api/v1/courses/<int:id>/', views.get_course),
    path(r'api/v1/article/', article_views.ArticleApiView.as_view()),
    path(r'api/v1/article/<int:id>/', article_views.article_item_view),
    path(r'api/v1/news/', news_view.NewsApiView.as_view()),
    path(r'api/v1/news/<int:id>/', news_view.NewsDetailView.as_view()),
]
