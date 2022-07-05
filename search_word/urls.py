from django.urls import path
from .views import detail_func
from . import views 

handler500 = views.my_customized_server_error
urlpatterns = [
  # 検索したい内容の入力
  path('',views.TopPageView.as_view(),name='top'),
  path('search_word/new/',views.CreateSearchWordView.as_view(),name='new_search_word'),
  path('search_words/', views.ListSearchWordView.as_view(),name='search_words'),

  path('suggest_result/<int:pk>/', detail_func, name='search_word'),
]