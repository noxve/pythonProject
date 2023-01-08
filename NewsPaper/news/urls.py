from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPost, CategoryListView, subscribe

urlpatterns = [
   path('', PostList.as_view(), name='news.html'),
   path('<int:pk>', PostDetail.as_view(), name='new.html'),
   path('search/', SearchPost.as_view(), name='search.html'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]