from django.urls import path , reverse
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    path('<slug:article>/', views.article, name='article'),
     path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
     path('<slug:slug>/', views.article, name='article'),

]
