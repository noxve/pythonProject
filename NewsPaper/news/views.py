from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView

from .models import *
from .filters import PostFilter
from .forms import PostForm



class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/news.html'
    context_object_name = 'poste'
    paginate_by = 10


class SearchPost(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news.html')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(ListView):
    models = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message= 'Вы успешно подписались на рассылку новостей категории: '
    return render(request, 'news/subscribe.html', {'category':category, 'message':message})



