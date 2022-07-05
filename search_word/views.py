from django.shortcuts import render
# request送信後redirect先を決める reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from .models import SearchWord
import pyperclip

from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError


class TopPageView(TemplateView):
    template_name = 'search_word/top.html'


class ListSearchWordView(ListView):
    template_name = 'search_word/search_word_list.html'
    model = SearchWord


class CreateSearchWordView(CreateView):
    template_name = 'search_word/search_word_create.html'
    model = SearchWord
    fields = {'category', 'technique',
              'error_message', 'error_detail', 'Feature'}
    success_url = reverse_lazy('search_words')


class SuggestWordView(DetailView):
    template_name = 'search_word/suggest_result.html'
    model = SearchWord


def suggest_word(words):
    # 提案ワードを格納する配列をオブジェクトの各要素を変数に定義
    suggest_word = []
    technique = words.technique
    error_message = words.error_message
    error_detail = words.error_detail
    Feature = words.Feature

    # 提案ワードを配列に格納
    suggest_word.append(technique + " " + error_detail)
    suggest_word.append(technique + " " + Feature)
    suggest_word.append(technique + " " + error_message)
    suggest_word.append(technique + " " + error_message + " " + error_detail)
    return suggest_word


def detail_func(request, pk):
    object = SearchWord.objects.get(pk=pk)
    suggest_result = suggest_word(object)
    print(suggest_result)
    # viewに渡す物を辞書型配列に変換
    context = {'object': object, 'suggest_result': suggest_result}

    if request.method == "POST":
        if "copy_word" in request.POST:
            print(request.POST["copy_word"])
            pyperclip.copy(request.POST["copy_word"])

    return render(request, 'search_word/suggest_result.html', context)
# Create your views here.

# 他の人が解決したワードとそのサイトURLを貼ってもらう。
# 自分の入力内容と解決した人の入力内容の近似値を求めページも出力できるようにするのがよさそう。


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
