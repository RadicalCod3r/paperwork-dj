from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from .models import (
    Article,
    Comment
)
from .forms import CommentForm

# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    template_name = 'articles/article_list.html'
    model = Article
    context_object_name = 'articles'

# class SingleArticleView(LoginRequiredMixin, DetailView):
#     template_name = 'articles/single_article.html'
#     model = Article
#     context_object_name = 'article'

class SingleArticleView(LoginRequiredMixin, View):
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        form = CommentForm

        return render(request, 'articles/single_article.html', {
            'article': article,
            'form': form,
            'comments': Comment.objects.all()
        })

    def post(self, request, slug):
        form = CommentForm(request.POST)
        article = Article.objects.get(slug=slug)

        if form.is_valid:
            form.instance.author = request.user
            form.instance.article = article
            form.save()

        return render(request, 'articles/single_article.html', {
            'article': article,
            'form': form,
            'comments': Comment.objects.all()
        })

class NewArticleView(LoginRequiredMixin, CreateView):
    template_name = 'articles/new_article.html'
    model = Article
    fields = ('title', 'content',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'articles/edit_article.html'
    model = Article
    fields = ('title', 'content',)

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user

class RemoveArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'articles/remove_article.html'
    model = Article
    success_url = reverse_lazy('article_list')

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user