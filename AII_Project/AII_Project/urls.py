"""AII_Project URL Configuration

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
from django.contrib import admin
from django.urls import path
from movies.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imdb_scrape/', imdb_scrape, name="imdb_scrape"),
    path('imdb_search/', imdb_search, name="imdb_search"),
    path('imdb_search_title/', imdb_search_title, name="imdb_search_title"),
    path('imdb_search_year/', imdb_search_year, name="imdb_search_year"),
    path('imdb_search_rating/', imdb_search_rating, name="imdb_search_rating"),
    path('imdb_search_all/', imdb_search_all, name="imdb_search_all"),
]
