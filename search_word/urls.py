from django.urls import path
from .views import detail_func
from . import views 
urlpatterns = [
  # 検索したい内容の入力
  path('',views.TopPageView.as_view(),name='top'),
  path('search_word/create/',views.CreateSearchWordView.as_view(),name='create_searchword'),
  path('search_words/', views.ListSearchWordView.as_view(),name='list_searchword'),

  path('suggest_result/<int:pk>/', detail_func, name='sugget_result'),
]