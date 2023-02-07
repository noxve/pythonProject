from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPost, CategoryListView, subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60*1)(PostList.as_view()), name='news.html'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='new.html'),
   path('search/', cache_page(60*5)(SearchPost.as_view()), name='search.html'),
   path('create/', cache_page(60*5)(PostCreate.as_view()), name='post_create'),
   path('<int:pk>/edit/', cache_page(60*5)(PostUpdate.as_view()), name='post_update'),
   path('<int:pk>/delete/', cache_page(60*5)(PostDelete.as_view()), name='post_delete'),
   path('categories/<int:pk>', cache_page(60*5)(CategoryListView.as_view()), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]