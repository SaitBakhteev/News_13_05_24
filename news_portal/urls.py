from django.urls import path, include
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostFilterView, create_post


urlpatterns = [
        path('', PostsList.as_view()),
        path('<int:pk>',PostDetail.as_view()),
        path('search/', PostFilterView.as_view()),
        path('test/', create_post,name='Create post'),
              ]