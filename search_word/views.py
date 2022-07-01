from django.shortcuts import render
# request送信後redirect先を決める reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView,TemplateView
from .models import SearchWord

class TopPageView(TemplateView):
  template_name = 'search_word/top.html'


class ListSearchWordView(ListView):
  template_name = 'search_word/search_word_list.html'
  model = SearchWord 

class CreateSearchWordView(CreateView):
  template_name = 'search_word/search_word_create.html'
  model = SearchWord 
  fields = {'category','technique','error_message','error_detail','Feature'}
  success_url = reverse_lazy('list_searchword')

class SuggestWordView(DetailView):
  template_name = 'search_word/suggest_result.html'
  model = SearchWord
  
def suggest_word(words):
  suggest_word = words.technique + " " + words.error_detail
  return suggest_word

def detail_func(request, pk):
  object = SearchWord.objects.get(pk=pk)
  suggest_result = suggest_word(object)
  print(suggest_result)
  # viewに渡す物を辞書型配列に変換
  context = {'object': object,'suggest_result':suggest_result}
  return render(request, 'search_word/suggest_result.html', context)


# Create your views here.


