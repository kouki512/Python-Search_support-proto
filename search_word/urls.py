from django.urls import path
from .views import detail_func,DeleteSearchWord
from . import views 

urlpatterns = [
  # 検索したい内容の入力
  path('',views.TopPageView.as_view(),name='top'),
  #path('search_word/new/',views.CreateSearchWordView.as_view(),name='new_search_word'),
  path('search_word/new/language',views.SelectLanguage,name='select_language'),
  path('search_word/new/errors',views.SelectErrors,name='select_errors'),
  path('search_words/', views.ListSearchWordView.as_view(),name='search_words'),
  path('suggest_result/<int:pk>/', detail_func, name='search_word'),
  path('search_words/<int:pk>/delete/',DeleteSearchWord,name='delete_search_words'),
]
# 正規表現⇒有効性を試す
# その後
# ベイズ、クラスタリング
