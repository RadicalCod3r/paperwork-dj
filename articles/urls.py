from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('new/', views.NewArticleView.as_view(), name='new_article'),
    path('<slug:slug>/edit/', views.EditArticleView.as_view(), name='edit_article'),
    path('<slug:slug>/remove/', views.RemoveArticleView.as_view(), name='remove_article'),
    path('<slug:slug>/', views.SingleArticleView.as_view(), name='single_article'),
]